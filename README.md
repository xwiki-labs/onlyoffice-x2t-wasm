Dockerfile building OnlyOffice x2t in WebAssembly using emscripten

```
cd x2t-wasm
docker build .
```

Individual modules

* x2t -> building onlyoffice x2t linux distribution
* emsdk -> build a docker environment for emscripten compilation
* onlyoffice -> full onlyoffice core linux build

