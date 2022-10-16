# Inference engine Endpoints

## Sanity check

* **URL**: `/`
* **Method**: `GET`
* **Data constraints**: No data required
* **Success Response**
  * **Code**: 200 OK
  * **Content example**:

    ```json
    {
        "TEST"
    }
    ```

## Check single exam

* **URL**: `/check-exam`
* **Method**: `POST`
* **Data constraints**:

  ```json
  {
      "exam_path": "[valid exam path]",
      "exam_name": "[valid exam name]"
  }
  ```

* **Data example**:

  ```json
  {
      "exam_path": "/1/1/",
      "exam_name": "1234567.jpg"
  }
  ```

* **Success Response**
  * **Code**: 200 OK
  * **Content example**:

    ```json
    {
      "Success!"
    }
    ```

## Check full exam

* **URL**: `/check-exams`
* **Method**: `POST`
* **Data constraints**:

  ```json
  {
      "exam_path": "[valid exam path]"
  }
  ```

* **Data example**:

  ```json
  {
      "exam_path": "/1/1/",
  }
  ```

* **Success Response**
  * **Code**: 200 OK
  * **Content example**:

    ```json
    {
      "Success!"
    }
    ```

## Generate exam key

* **URL**: `/generate-exam-key`
* **Method**: `POST`
* **Data constraints**:

  ```json
  {
      "exam_path": "[valid exam path]"
  }
  ```

* **Data example**:

  ```json
  {
      "exam_path": "/1/1/"
  }
  ```

* **Success Response**
  * **Code**: 200 OK
  * **Content example**:

    ```json
    {
      "Success!"
    }
    ```
