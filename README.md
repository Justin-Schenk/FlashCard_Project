Remove Task Microservice

Description
The Remove Task Microservice processes DELETE requests to remove tasks from the data.tsv file based on a unique task ID. It is part of a larger task management application.

How to Use the Remove Microservice
Endpoint:

URL: http://localhost:8002/remove/:id
Method: DELETE
Request:

Replace :id with the unique task ID to be removed.

Example request using curl:

curl -X DELETE http://localhost:8002/remove/cm35mfl9b0004m0ic6zu1h5vo

Response:
Success:

Updates the data.tsv contents on the client side with the task removed. Returns the new list.
Example of returned data.tsv contents:
[{"id":"cm35mfl9b0004m0ic6zu1h5vo","title":"Do my homework","status":"In Progress"}
{"id":"cm35mgqio0005m0icbc908ew0","title":"Review lecture notes","status":"In Progress"}
{"id":"cm35mgubq0006m0ic0vro710s","title":"Prepare for midterm","status":"In Progress"}
{"id":"cm36zemao000nm0icfy5vcp02","title":"Meet with my study group","status":"In Progress"}
{"id":"cm3p3jcpc000304eqgc155kqd","title":"Wash Dishes","status":"In Progress"}]

Error (Task Not Found):
{
  "error": "Task not found."
}

Communication Contract

How to Send Data:

Use a DELETE request to the endpoint /remove/:id where :id is the unique task identifier.

Example request:

DELETE http://localhost:8002/remove/<task-id>

How to Receive Data:

The service returns a JSON response indicating success or failure.

Testing the Microservice:

Use Postman or curl to send DELETE requests to the service.

Verify task removal in the data.tsv file.

UML:
![image](https://github.com/user-attachments/assets/fdfeec8b-6fee-4d1d-bd4c-d2e2fe1a3ad0)

