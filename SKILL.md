---
name: deep-unit-test
description: Generates and audits high-value, real-coverage unit tests following Vladimir Khorikov's principles (Unit Testing Principles, Practices, and Patterns) and BDD Given-When-Then. Strictly prevents shallow AI testing (SUT-mocking cheats) and ensures real domain logic is verified against injected collaborators.
version: 1.0.0
author: redlittlewall
---

# Deep Unit Test (deep-unit-test)

A standard for autonomous AI agents and human engineers to author unit tests that provide **genuine regression protection** and **resistance to refactoring**, eliminating the "Shallow AI Test Trap".

## 1. The Core Philosophy (Vladimir Khorikov's 4 Pillars)

A test is only valuable if it maximizes all 4 pillars:

1. **Protection Against Regressions:** The test must execute the *real* code of the System Under Test (SUT). If a bug is introduced into the SUT, the test MUST fail.
2. **Resistance to Refactoring:** The test must verify **observable business outcomes and collaborator contracts**, NOT private implementation details. Refactoring internal code without changing behavior must not break the test.
3. **Fast Feedback:** Runs in milliseconds using isolated in-memory test doubles for out-of-process dependencies.
4. **Maintainability:** Clear Arrange-Act-Assert (Given-When-Then) structure with minimal boilerplate.

---

## 2. Inviolable Rule: The Anti-SUT Mocking Law

> **NEVER MOCK THE SUT.**

### The "Shallow AI Test" Trap:
When asked to write unit tests, LLMs frequently take a lazy shortcut:
```typescript
// ❌ CRITICAL CHEAT: Mocking the method you are supposed to test!
jest.spyOn(service, 'reclassify').mockResolvedValue(fakeResult);
const res = await service.reclassify('admin-1', 'tattoo-1');
expect(res).toBe(fakeResult); // 100% false coverage, 0% real logic tested!
```
This is a **testing fraud**. The real method body was never executed. If someone deletes the entire method body, this test still passes!

### The Deep Unit Test Standard:
```typescript
// ✅ REAL TEST: Real SUT execution, isolated injected dependencies
// Given (Arrange)
tattooRepository.findOne.mockResolvedValue(mockTattoo);
photoRepository.find.mockResolvedValue([mockPhoto]);
awsS3Service._getPresignedUrl.mockResolvedValue('https://s3/test.jpg');
aiVisionService.classifyTattoo.mockResolvedValue(mockAiResult);
createTattooDetailsService.create.mockResolvedValue(undefined);

// When (Act) - Executing the REAL service method
const result = await service.reclassify('admin-1', 'tattoo-1');

// Then (Assert) - Verifying observable outcomes & collaborator calls
expect(result).toEqual(mockAiResult);
expect(createTattooDetailsService.create).toHaveBeenCalledWith(
  expect.anything(),
  expect.anything(),
  expect.anything(),
  expect.anything(),
  mockAiResult.bodyPartId,
  mockAiResult.sizeId,
  expect.anything(),
  undefined,
  'tattoo-1'
);
```

---

## 3. Universal Test Authoring Workflow

Follow this 4-step sequence for every unit test:

### Step 1: Identify the SUT & Collaborators
- **SUT:** The target class/function under test. It is instantiated for real.
- **Injected Collaborators:** Repositories, HTTP clients, external services injected in the constructor. These are replaced with minimal test doubles (mocks/stubs).

### Step 2: Deterministic Module Scaffolding
- Generate the testing module, test double providers, and instance retrieval before writing test cases.
- In NestJS: Use `Test.createTestingModule({ providers: [SUT, ...mocks] })`.
- In Flutter: Use `MockTail` or `Mockito` for injected repositories.

### Step 3: Given-When-Then BDD Scenarios
For every public method:
1. **Happy Path:** Valid inputs produce expected outputs and trigger expected collaborator side-effects.
2. **Boundary / Null Paths:** Missing entities, empty lists, or invalid states throw expected domain exceptions (e.g., `NotFoundException`, `UnprocessableEntityException`).
3. **Sad Path (Collaborator Errors):** Failures in downstream services are handled or bubbled up appropriately.

### Step 4: Quality Gate Verification
Run the native test suite with code coverage:
- **Line Coverage:** Must achieve $\ge 60\%$ on the target file.
- **Anti-Cheat Scan:** Grep for forbidden patterns:
  - `spyOn(service, ...)`
  - `spyOn(sut, ...)`
  - `service.<method> = jest.fn()`
If detected, reject immediately.

---

## 4. Framework Profiles

### NestJS (TypeScript + Jest)
- **Scaffold:** `Test.createTestingModule`.
- **Strict Mocking Rule:** In TypeScript strict mode, always pass explicit arguments:
  ```typescript
  mockFn.mockResolvedValue(undefined); // NOT mockResolvedValue()
  repository.findOne.mockResolvedValue(null); // NOT undefined
  ```
- **Execution:** `npx jest --coverage --collectCoverageFrom=<source_file> <spec_file>`.

### Flutter (Dart + `package:test`)
- **Scaffold:** `setUp(() { sut = MyService(mockRepo); })`.
- **Mocking:** `when(() => mockRepo.fetch()).thenAnswer((_) async => data);`.
- **Execution:** `dart test --coverage=coverage <test_file>`.

### Svelte / Web (TypeScript + Vitest)
- **Scaffold:** In-memory store/service instantiation.
- **Execution:** `npx vitest run --coverage <test_file>`.
