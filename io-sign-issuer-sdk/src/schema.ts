import {
  DossierDetailView,
  SignatureRequestDetailView,
  GetRequestsByDossierRequest,
  DocumentMetadata,
} from "@io-sign/io-sign-api-client";

export type SdkSchema = {
  fiscalCode?: string;
  signatureRequest?: Partial<SignatureRequestDetailView>;
  dossier?: Partial<DossierDetailView>;
  signatureRequests?: Partial<GetRequestsByDossierRequest>;
  documentsPaths?: string[];
  documentsMetadata?: Array<DocumentMetadata>;
};

export type SdkSchemaWithSignatureRequest = SdkSchema & {
  signatureRequest: SignatureRequestDetailView;
};

export type SdkSchemaWithDossier = SdkSchema & {
  dossier: DossierDetailView;
};
