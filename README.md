# Keymitt Task


### Testing flow:

1. Clone project
2. Create .env file in main directory with virtual envs, file must look like below
    ```
        HOST=0.0.0.0
        PORT=5000
        DB_NAME=smart_lock
        DB_HOST=db
        DB_PORT=27017
    ```
3. Run command in terminal for starting container with project
    ```
    docker-compose up --build
    ```
4. POST http://0.0.0.0:5000/application/ as form-data
        with body 
   ```
   {
        file: "filedata",
        version: 5.5
   }
   ```
5. GET http://0.0.0.0:5000/application/?version=4.8


