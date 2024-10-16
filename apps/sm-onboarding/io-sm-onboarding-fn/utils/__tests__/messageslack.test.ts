import { isRight } from "fp-ts/lib/Either";
import { DecodedContract } from "../messageslack";

describe("Test decoder", () => {
  it("should be validate a valid item", () => {
    const inputData = {
      createdAt: "2024-05-01T00:00:00Z",
      updatedAt: "2024-05-01T00:00:00Z",
      institution: {
        description: "test",
        origin: "origin",
        originId: "originId",
        taxCode: "taxCode"
      },
      internalIstitutionID: "internalIstitutionID",
      notificationType: "ADD",
      product: "prod-io-premium"
    };
    const res = DecodedContract.decode(inputData);
    expect(isRight(res)).toBe(true);
  });
  it("should be validate an item with pricing plan", () => {
    const inputData = {
      createdAt: "2024-05-01T00:00:00Z",
      updatedAt: "2024-05-01T00:00:00Z",
      institution: {
        description: "test",
        origin: "origin",
        originId: "originId",
        taxCode: "taxCode"
      },
      internalIstitutionID: "internalIstitutionID",
      notificationType: "ADD",
      product: "prod-io-premium",
      pricingPlan: "FA"
    };
    const res = DecodedContract.decode(inputData);
    expect(isRight(res)).toBe(true);
  });
  it("should not be validate an unknown product id", () => {
    const inputData = {
      institution: {
        description: "test"
      },
      product: "prod-io-standard"
    };
    const res = DecodedContract.decode(inputData);
    expect(isRight(res)).toBe(false);
  });
});
