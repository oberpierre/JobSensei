# LLM

Due to cost considerations, we are employing our own large language model (LLM), in this case llama2.
However, you may adapt the project using a different model or API.
Do note that based on the chosen model or service, there may be varying input/output token limitations, so you may have to further tune the project to your setup and needs. Some considerations (aside from the model) are:

- Optimizing prompts to the model
- CV/Job listing provision (you may run a preparation step performing summarization/extraction of relevant data)

## Getting Started

### Model Preparation

Before building, download the llama2 model from [huggingface.co](https://huggingface.co/meta-llama) and place it in the `model/llama2` folder. Choose between the 7B, 13B, and 70B based on your needs and hardware constraints.

### llama.cpp

We employ the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) project to increase the performance (in terms of token generation) of our LLM. This library is designed for running models, including llama2, with optimized quantization methods. Out of the box, we have configured it for `q4_0` quantization, but you might want to select a different quantization method based on your target platform and hardware. See [llama.cpp's quantization section](https://github.com/ggerganov/llama.cpp#quantization) for more detailed benchmarks and trade-offs.

### Building

1. Make sure to provide your model files (directly) in the model/llama2 folder
1. Run `bazel build //llm:conversion` to run quantization
