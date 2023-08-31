# JobSensei

![Build Status](https://github.com/oberpierre/JobSensei/actions/workflows/build.yml/badge.svg)

JobSensei is your wise and helpful guide on your job-hunting journey. With JobSensei by your side, you'll navigate the world of job listings with the insight of a master!

## Vision

JobSensei aims to land you your next job by:

- **Job Board Crawling & Alerting**: Continuously crawls job boards for the latest listings and alerts you so you may take advantage of every opportunity.
- **Intelligent Matching**: Using large language models, JobSensei assesses job listings against your profile, assigning a suitability score.
- **Spruce up your CV**: Tailors your master CV for each opportunity, emphasizing skills, fine-tuning wording, and reshuffling details to resonate with the job description.

## Getting Started

1. **Setup Bazel**: If you don't have Bazel installed, follow the [Bazel Getting Started Guide](https://bazel.build/start) to get it set up.
2. **Clone the Repository**:

   ```
   git clone https://github.com/oberpierre/JobSensei.git
   cd JobSensei
   ```

3. **Build using Bazel**:

   Follow the [model preparation instructions](./llm/README.md#model-preparation) in the llm package. Once the model is provided you can build the whole project by running the following command in the root of the project:

   ```
   bazel build //...
   ```

4. **Testing**:

   Run all tests using:

   ```
   bazel test //...
   ```

   or for a single target:

   ```
   bazel test <target>
   ```

That's it! You can deploy the binaries now or run JobSensei on your local machine using `bazel run <target>`.

## Contribute

Help make JobSensei even better! If you have suggestions, encounter bugs, or wish to improve the platform, please open an issue or send over a pull request.
