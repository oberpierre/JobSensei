load("@rules_python//python:pip.bzl", "compile_pip_requirements")

# This rule adds a convenient way to update the requirements file.
compile_pip_requirements(
    name = "requirements",
    extra_args = ["--allow-unsafe"],
    requirements_in = "//third-party:requirements.in",
    requirements_txt = "//third-party:requirements_lock.txt",
)
