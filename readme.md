# dcm-anon

Custom Dicom anonymizer that plays nicely with:
- FreeSurfer
- thinq/rethinq
- AutoRegsiter

Tags required for FreeSurfer recons (scanner manufacturer, etc) are left untouched

Tags required for thinq/rethinq recons (age, sex, scanner manufactuer, feild stregth) are left untouched.

PatientID tag is anonymized with a one-to-one map so that autoregister queries will work

## Usage


## Anonimization procedure

The following tags are replaced with their md5sum hash:
- 0008,1030: StudyDescription
- 0008,1070: OperatorsName
- 0010,0010: PatientName
- 0010,0020: PatientID
- 0032,1060: RequestedProcedureDescription
- 0040,0254: PerformedProcedureStepDescription

An arbitrary datestring, `19991231`, is generated and used to replace the datestring in the following feilds:
- 0008,0012 InstanceCreationDate
- 0008,0018 SOPInstanceUID
- 0008,0020 StudyDate
- 0008,0021 SeriesDate
- 0008,0022 AcquisitionDate
- 0008,0023 ContentDate
- 0029,1009 CSAImageHeaderVersion
- 0029,1019 CSASeriesHeaderVersion
- 0040,0244 PerformedProcedureStepStartDate
- 0040,0253 PerformedProcedureStepID
- 0020,000e SeriesInstanceUID
- 0020,0052 FrameOfReferenceUID
- 0008,1140 ReferencedImageSequence
