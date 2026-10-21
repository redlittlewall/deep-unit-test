# 🏛️ Vladimir Khorikov's 4 Pillars of a Good Unit Test

Extracted and adapted from *Unit Testing Principles, Practices, and Patterns* by Vladimir Khorikov.

---

### Pillar 1: Protection Against Regressions
- **Definition:** The ability of a test to detect bugs introduced into the codebase.
- **Key Determinants:**
  - Amount of code executed during the test (more code = higher protection).
  - Complexity of the domain logic executed.
  - The test must fail if the business logic inside the SUT is altered or broken.

---

### Pillar 2: Resistance to Refactoring
- **Definition:** The degree to which a test can sustain a refactoring of the underlying code without raising a false alarm (false positive).
- **The Metric of Excellence:**
  - Tests should verify **the observable end-result (the WHAT)**, not the internal steps or private method calls (the HOW).
  - Tightly coupled tests that assert every private method call break every time code is refactored, creating developer fatigue and abandonment of the test suite.

---

### Pillar 3: Fast Feedback
- **Definition:** Tests must execute in milliseconds so that developers and CI pipelines run them on every save or commit.
- **Optimization Strategy:**
  - Replace network calls, disk I/O, and external databases with in-memory test doubles (fakes, stubs, mocks).
  - Reserve slow integration tests for out-of-process boundaries.

---

### Pillar 4: Maintainability
- **Definition:** How easy it is for a developer to read, understand, and modify the test.
- **Guidelines:**
  - Keep tests concise.
  - Use Given-When-Then structure.
  - Do not duplicate complex domain logic inside the test.
