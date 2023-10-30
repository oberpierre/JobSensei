load("@rules_foreign_cc//foreign_cc:defs.bzl", "make")
load("@llm_deps//:requirements.bzl", "all_requirements")

filegroup(
    name = "sources",
    srcs = glob(["**"]),
)

make(
    name = "llama_cpp_bins",
    lib_source = ":sources",
    out_binaries = [
        "main",
        "quantize",
    ],
    args = [
        "-E CXXFLAGS:=-std=c++11",
    ],
    env = {
        "CC": "/usr/bin/gcc",
        "CXX": "/usr/bin/g++",
        "LLAMA_CUBLAS": "1",
    },
    postfix_script = "cp main quantize $INSTALLDIR/bin/",
    targets = [
        "main",
        "quantize",
    ],
)

genrule(
    name = "main",
    srcs = [":llama_cpp_bins"],
    outs = ["mainbin"],
    cmd = "cp `ls $(locations :llama_cpp_bins) | grep main$$` $(@)",
    executable = True,
    visibility = ["//visibility:public"]
)

genrule(
    name = "quantize",
    srcs = [":llama_cpp_bins"],
    outs = ["quantizebin"],
    cmd = "cp `ls $(locations :llama_cpp_bins) | grep quantize$$` $(@)",
    executable = True,
    visibility = ["//visibility:public"]
)

py_binary(
    name = "convert",
    srcs = [":sources"],
    deps = all_requirements,
    visibility = ["//visibility:public"]
)
