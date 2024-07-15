function transform(line) {
  // Split the input line by commas to extract individual values
  var values = line.split(",");

  // Create an empty JavaScript object to store the values
  var obj = {};

  // Assign values to the object properties based on their position in the input string
  obj.ID = values[0];
  obj.Status = values[1];
  obj.Event = values[2];
  obj.Details = values[3];
  obj.City = values[4];
  obj.State = values[5];
  // Parse the dates using parseDate function
  obj.Start_Date = values[6];
  obj.End_Date = values[7];

  // Convert the JavaScript object to a JSON string
  var jsonString = JSON.stringify(obj);

  // Return the JSON string
  return jsonString;
}
