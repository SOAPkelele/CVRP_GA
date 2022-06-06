import requests


def download():
    test_cases = [
        "A/A-n32-k5",
        "A/A-n39-k5",
        "E/E-n22-k4",
        "F/F-n45-k4",
        "P/P-n22-k8",
        "tai/tai75b",
        "P/P-n22-k2",
        "B/B-n31-k5",
        "CMT/CMT1",
        "P/P-n16-k8"
    ]

    base_url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances"

    s = requests.Session()

    for case in test_cases:
        url = f"{base_url}/{case}"

        data = s.get(f"{url}.vrp")
        solution = s.get(f"{url}.sol")

        case_type = case.split("/")[-1]

        with open(f"data/{case_type}.data", "w") as f:
            f.write(data.text)

        with open(f"data/{case_type}.sol", "w") as f:
            f.write(solution.text)


if __name__ == "__main__":
    download()
