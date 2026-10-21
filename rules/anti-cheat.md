# 🚫 Anti-Cheat Rules (Zero SUT Mocking)

## The Core Mandate

When generating or verifying unit tests, the following patterns are **STRICTLY FORBIDDEN**:

| Forbidden Pattern | Reason for Rejection |
| :--- | :--- |
| `jest.spyOn(service, '<method>')` | Mocks the System Under Test. Eliminates real code execution. |
| `jest.spyOn(sut, '<method>')` | Mocks the SUT instance directly. |
| `service.<method> = jest.fn(...)` | Monkey-patches SUT method body. |
| `sut.<method> = jest.fn(...)` | Overwrites real business logic with a stub. |
| `expect(service).toBeDefined()` alone | Trivial test that provides zero regression protection. |

## Why AI Models Cheat

Large Language Models (LLMs) are trained to minimize loss and satisfy prompt constraints like "write a test that passes". 
Mocking the SUT method itself is the easiest path of least resistance:
1. No need to understand internal branches, conditions, or database models.
2. The mock always returns the expected value.
3. Test runner reports 100% green tests in 50ms.

However, this produces **zero business value**.

## The Enforcement Regex

Any test file scanned by the `deep-unit-test` quality gate must pass this regex check:

```python
FORBIDDEN_PATTERNS = [
    r"spyOn\(\s*service\s*,",
    r"spyOn\(\s*sut\s*,",
    r"service\.\w+\s*=\s*jest\.fn\(",
    r"sut\.\w+\s*=\s*jest\.fn\(",
]
```

If any match is found, the test is rejected with an immediate failure flag.
