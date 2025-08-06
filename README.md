# Amazon Idle Benchmarking Tool

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-informational)

A tool designed to benchmark and analyze idle resource consumption and performance on using AWS QuickSight. Must have personal webhook and site data for use.

---


## Features

- **Automated Benchmarking:** Easily run predefined benchmark tests against various AWS services.
- **Cost Analysis:** Track and report on the costs associated with idle resources.
- **Performance Metrics:** Collects essential performance data like CPU utilization, memory usage, and network I/O.
- **Customizable:** Easily extend the tool to benchmark other services or custom configurations.
- **Reproducible Results:** Ensures consistent and reliable benchmark results through standardized configurations.

## Prereqs

- An active AWS Account with appropriate permissions.
- [AWS CLI](https://aws.amazon.com/cli/) configured on your local machine.
- [Python 3.8+](https://www.python.org/downloads/) with `pip`.
- Task scheduler for local automation.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/AmazonBenchmarkingWorkflow.git](https://github.com/your-username/AmazonBenchmarkingWorkflow.git)
    cd AmazonBenchmarkingWorkflow
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
## Contributing

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/dopeCrap`)
3.  Commit your Changes (`git commit -m 'Add some dope shit'`)
4.  Push to the Branch (`git push origin feature/cool`)
5.  Open a Pull Request

## License

MIT License.

