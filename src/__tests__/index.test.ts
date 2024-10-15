import { somma } from ".."

describe("Somma suite test", () => {
  it("should be return a sum", () => {
    expect(somma(2,3)).toBe(5)
  })
})