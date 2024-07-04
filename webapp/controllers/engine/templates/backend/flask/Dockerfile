FROM python:3.10-alpine

# Create and set the working directory 'project' should be the name of your project
WORKDIR /project

# Install dependencies
RUN pip install poetry

# Copy the entire application code
COPY . .

# Install the application dependencies
RUN poetry install

# Expose the port your application will run on
EXPOSE 5000

# Specify the command to run on container start
CMD ["python", "src/app/__main__.py"]