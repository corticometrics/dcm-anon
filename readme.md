# dcm-anon

Custom Dicom anonymizer that plays nicely with:
- FreeSurfer
- thinq/rethinq
- AutoRegsiter

Tags required for FreeSurfer recons (scanner manufacturer, etc) are left untouched

Tags required for thinq/rethinq recons (age, sex, scanner manufactuer, feild stregth) are left untouched.

PatientID tag is anonymized with a one-to-one map so that autoregister queries will work

## Usage

`./dcm-anon in-dir out-dir`

## Anonimization procedure

The following tags are replaced with their md5sum hash:
- 0008,0080: InstitutionName
- 0008,0081: InstitutionAddress
- 0008,1030: StudyDescription
- 0008,1070: OperatorsName
- 0010,0010: PatientName
- 0010,0020: PatientID
- 0032,1060: RequestedProcedureDescription
- 0040,0254: PerformedProcedureStepDescription

An arbitrary datestring, `19991231`, is generated. It is used to overwrite the datesetings in the following tags:
- 0010,0030 PatientBirthDate
- 0008,0012 InstanceCreationDate
- 0008,0020 StudyDate
- 0008,0021 SeriesDate
- 0008,0022 AcquisitionDate
- 0008,0023 ContentDate
- 0040,0244 PerformedProcedureStepStartDate
- 0002,0003 MediaStorageSOPInstanceUID

If the original InstanceCreationDate is found embedded in the following tags, it is also replaced with `19991231`.
- 0008,0018 SOPInstanceUID
- 0029,1009 CSAImageHeaderVersion
- 0029,1019 CSASeriesHeaderVersion
- 0040,0253 PerformedProcedureStepID
- 0020,000e SeriesInstanceUID
- 0020,0052 FrameOfReferenceUID
- 0008,1140 ReferencedImageSequence

If the filename contains the datesting, that is replaced with `19991231` in the output filename as well.
