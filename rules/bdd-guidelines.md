# 📐 Given-When-Then BDD Guidelines

Every test case authored under `deep-unit-test` must strictly follow the 3-phase BDD format:

```typescript
it('should perform expected action when conditions are met', async () => {
  // 1. Given (Arrange): Configure test doubles and inputs
  // - Prepare input fixtures
  // - Program injected mocks to return expected test doubles
  
  // 2. When (Act): Invoke the REAL method on the SUT
  // - Execute: const result = await service.myMethod(input);
  
  // 3. Then (Assert): Verify observable outcomes
  // - Verify return value: expect(result).toEqual(expected);
  // - Verify state change / collaborator contract: expect(repo.save).toHaveBeenCalledWith(...);
});
```

## Mandatory Scenarios Per Public Method:

1. **Happy Path (Sucesso):**
   - Inputs are valid.
   - Collaborators return healthy data.
   - SUT executes business logic to completion.

2. **Boundary & Validation Paths (Exceções de Domínio):**
   - Entity not found: Collaborator returns `null` -> SUT throws `NotFoundException`.
   - Missing prerequisites: SUT throws `UnprocessableEntityException` or `BadRequestException`.

3. **Error Escalation (Falha de Colaborador):**
   - Injected service rejects with network error -> SUT bubbles up or handles cleanly.
