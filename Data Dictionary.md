# Data Dictionary — Intelligent Vehicle Violation Detection and Monitoring System

| **Field Name**           | **Type**       | **Size**       | **Description**                                              | **Example**           |
|--------------------------|---------------|---------------|--------------------------------------------------------------|---------------------|
| CameraID                 | String        | 20            | Unique identifier for each camera                            | CAM_001             |
| VideoStream              | Blob / Video  | N/A           | Real-time video feed captured from camera                    | N/A                 |
| VehicleType              | String        | 20            | Type of detected vehicle                                      | Bus                 |
| SafetyClassification     | String        | 10            | Classification of vehicle safety                             | Unsafe              |
| PersonCount              | Integer       | 3             | Estimated number of persons around/on the vehicle           | 3                   |
| NumberPlateRegion        | Boolean        | 1            | vehicle number plate in the image                            | True               |
| NumberPlateText          | String        | 15            | Recognized vehicle number plate                               | ABC-1234            |
| ViolationTimestamp       | DateTime      | N/A           | Date and time of violation detection                         | 2025-10-25 14:35    |
| GPSLocation              | String        | 30            | GPS coordinates of camera location                           | 33.6844,73.0479     |
| Snapshot                 | Blob / Image  | N/A           | Image snapshot of vehicle during violation                   | N/A                 |
| AdminUsername            | String        | 30            | Username used by admin to login                               | admin123            |
| AdminPassword            | String        | 50            | Password used by admin to login                               | ••••••••            |
| AdminSessionToken        | string        | 32            | JWT Token to authenticate the request is from admin           | sdjfhlskjdhflskjdhf |
| FilterCriteria           | String / JSON | 100           | Criteria applied to filter violation records                 | {"Location":"City","Date":"2025-10-25"} |
| SelectedViolationRecord  | JSON / Object | N/A           | Specific violation record selected by admin                  | N/A                 |
| DeletionConfirmed        | Boolean       | 1             | Flag indicating if deletion of violation record is confirmed | True                |
