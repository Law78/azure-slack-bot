/* eslint-disable no-console */
import { isRight } from "fp-ts/lib/Either";
import { DecodedContract } from "../../utils/messageslack";

/* eslint-disable sort-keys */

describe("Handler", () => {
  it("Should decode", () => {
    const rawContract = {
      id: "11111111",
      internalIstitutionID: "11111-11-1-11111",
      product: "prod-interop-atst",
      state: "ACTIVE",
      filePath: "PATH/TO/Adesione.pdf",
      fileName: "signed_o_adesione.pdf",
      onboardingTokenId: "111111",
      institution: {
        institutionType: "PA",
        description: "Comune di xxxxx",
        digitalAddress: "mail@dom.regione.it",
        address: "Viale Roma, 1",
        taxCode: "12345678901",
        origin: "IPA",
        originId: "1_1111",
        zipCode: "00000",
        istatCode: "000000",
        city: "ROMA",
        country: "IT",
        county: "SI",
        category: "L6"
      },
      billing: {
        vatNumber: "1111111111",
        publicServices: false,
        recipientCode: "123"
      },
      // eslint-disable-next-line sonarjs/no-duplicate-string
      createdAt: "2024-06-25T13:57:14.031Z",
      updatedAt: "2024-06-25T13:57:14.031Z",
      notificationType: "ADD"
    };

    const res = DecodedContract.decode(rawContract);
    expect(isRight(res)).toBe(true);
  });
  it("Should decode as UPDATE", () => {
    const rawContract = {
      id: "11111111",
      internalIstitutionID: "11111-11-1-11111",
      product: "prod-interop-atst",
      state: "ACTIVE",
      filePath: "PATH/TO/Adesione.pdf",
      fileName: "signed_o_adesione.pdf",
      onboardingTokenId: "111111",
      institution: {
        institutionType: "PA",
        description: "Comune di xxxxx",
        digitalAddress: "mail@dom.regione.it",
        address: "Viale Roma, 1",
        taxCode: "12345678901",
        origin: "IPA",
        originId: "1_1111",
        zipCode: "00000",
        istatCode: "000000",
        city: "ROMA",
        country: "IT",
        county: "SI",
        category: "L6"
      },
      billing: {
        vatNumber: "1111111111",
        publicServices: false,
        recipientCode: "123"
      },
      createdAt: "2024-06-25T13:57:14.031Z",
      updatedAt: "2024-06-25T14:03:54.031Z",
      notificationType: "ADD"
    };

    const res = DecodedContract.decode(rawContract);
    expect(isRight(res)).toBe(true);
    if (isRight(res)) {
      const diff = Math.abs(
        (new Date(res.right.updatedAt).getTime() -
          new Date(res.right.createdAt).getTime()) /
          1000 /
          60
      );
      expect(diff).toBeGreaterThan(5);
    }
  });
});
