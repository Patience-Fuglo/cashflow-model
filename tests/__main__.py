"""Run all project tests without pytest."""
from importlib import import_module

TEST_MODULES = [
    "tests.test_cf1",
    "tests.test_cf2",
    "tests.test_cf3",
    "tests.test_cf4",
    "tests.test_cf5",
    "tests.test_cf6",
    "tests.test_download_integration",
]


def main():
    failures = 0
    for module_name in TEST_MODULES:
        module = import_module(module_name)
        print(f"\n=== {module_name} ===")
        exit_code = module.run_module_tests(module.__dict__)
        if exit_code != 0:
            failures += 1

    print("\n=== SUMMARY ===")
    if failures == 0:
        print("All modules passed.")
        return 0

    print(f"{failures} module(s) had failures.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
