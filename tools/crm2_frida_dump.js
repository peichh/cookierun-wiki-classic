// ponytail: narrow hook; add GetMapData-specific hook only if zlib path misses.
const dumpDir = "/sdcard/Download/cookierun_crm2_dumps";
const activeFds = new Set();
const activeAssets = new Set();
let activeMap = null;
let seq = 0;

function cstr(p) {
  return p.isNull() ? "" : p.readCString();
}

function sh(cmd) {
  try {
    const system = new NativeFunction(Module.findExportByName(null, "system"), "int", ["pointer"]);
    const s = Memory.allocUtf8String(cmd);
    system(s);
  } catch (_) {}
}

function dump(ptr, len, tag) {
  if (!activeMap || ptr.isNull() || len <= 16) return;
  sh(`mkdir -p ${dumpDir}`);
  const safe = activeMap.replace(/[^A-Za-z0-9_.-]/g, "_");
  const path = `${dumpDir}/${safe}.${tag}.${seq++}.bin`;
  const f = new File(path, "wb");
  f.write(ptr.readByteArray(len));
  f.flush();
  f.close();
  console.log(`[crm2] dumped ${len} bytes -> ${path}`);
}

function hookOpen(name) {
  const p = Module.findExportByName(null, name);
  if (!p) return;
  Interceptor.attach(p, {
    onEnter(args) {
      this.path = cstr(args[0]);
    },
    onLeave(ret) {
      const fd = ret.toInt32();
      if (fd >= 0 && this.path.includes("MapData_") && this.path.includes(".crm2")) {
        activeFds.add(fd);
        activeMap = this.path.split("/").pop();
        console.log(`[crm2] open ${fd} ${activeMap}`);
      }
    },
  });
}

function hookClose() {
  const p = Module.findExportByName(null, "close");
  if (!p) return;
  Interceptor.attach(p, {
    onEnter(args) {
      const fd = args[0].toInt32();
      if (activeFds.has(fd)) {
        activeFds.delete(fd);
        console.log(`[crm2] close ${fd}`);
      }
    },
  });
}

function hookUncompress() {
  const p = Module.findExportByName(null, "uncompress");
  if (!p) return console.log("[crm2] zlib uncompress export not found");
  Interceptor.attach(p, {
    onEnter(args) {
      this.dest = args[0];
      this.destLenPtr = args[1];
      this.enabled = !!activeMap;
    },
    onLeave(ret) {
      if (!this.enabled || ret.toInt32() !== 0) return;
      dump(this.dest, this.destLenPtr.readULong(), "uncompress");
    },
  });
  console.log("[crm2] hooked uncompress");
}

function hookInflate() {
  const p = Module.findExportByName(null, "inflate");
  if (!p) return console.log("[crm2] zlib inflate export not found");
  Interceptor.attach(p, {
    onEnter(args) {
      this.z = args[0];
      this.enabled = !!activeMap;
      this.out = this.z.add(24).readPointer();
    },
    onLeave(ret) {
      if (!this.enabled || ret.toInt32() !== 1) return; // Z_STREAM_END
      const end = this.z.add(24).readPointer();
      dump(this.out, end.sub(this.out).toInt32(), "inflate");
    },
  });
  console.log("[crm2] hooked inflate");
}

hookOpen("open");
hookOpen("open64");
hookOpen("__open_2");
hookClose();
hookUncompress();
hookInflate();

const openat = Module.findExportByName(null, "openat");
if (openat) {
  Interceptor.attach(openat, {
    onEnter(args) {
      this.path = cstr(args[1]);
    },
    onLeave(ret) {
      const fd = ret.toInt32();
      if (fd >= 0 && this.path.includes("MapData_") && this.path.includes(".crm2")) {
        activeFds.add(fd);
        activeMap = this.path.split("/").pop();
        console.log(`[crm2] openat ${fd} ${activeMap}`);
      }
    },
  });
}

const assetOpen = Module.findExportByName("libandroid.so", "AAssetManager_open");
if (assetOpen) {
  Interceptor.attach(assetOpen, {
    onEnter(args) {
      this.path = cstr(args[1]);
    },
    onLeave(ret) {
      if (!ret.isNull() && this.path.includes("MapData_") && this.path.includes(".crm2")) {
        activeAssets.add(ret.toString());
        activeMap = this.path.split("/").pop();
        console.log(`[crm2] asset open ${activeMap}`);
      }
    },
  });
}

const assetRead = Module.findExportByName("libandroid.so", "AAsset_read");
if (assetRead) {
  Interceptor.attach(assetRead, {
    onEnter(args) {
      this.asset = args[0].toString();
      this.buf = args[1];
    },
    onLeave(ret) {
      if (activeAssets.has(this.asset) && ret.toInt32() > 0) {
        // encrypted chunks; useful sanity check if zlib hooks never fire.
        dump(this.buf, ret.toInt32(), "asset-read");
      }
    },
  });
}

const assetClose = Module.findExportByName("libandroid.so", "AAsset_close");
if (assetClose) {
  Interceptor.attach(assetClose, {
    onEnter(args) {
      const key = args[0].toString();
      if (activeAssets.has(key)) {
        activeAssets.delete(key);
        console.log("[crm2] asset close");
      }
    },
  });
}
console.log("[crm2] hook loaded");
