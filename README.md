# EMIS data engineer assessment pipeline

### Description

<p>This containerised pipeline takes data using the FHIR standard from the EMIS repository in GitHub and tranforms it into a more workable format in a MongoDB client.</p>

### Tools Used

<p>This pipeline uses Python and a Docker container.</p> 

<p>The pipeline is handled using DVC, this allows data versions to be tracked with Git (however this is not being utilised in this example), it is primarily being used to define and orchestrate the pipeline and allows stages to eb skipped if there have been no changes in the dependencies. It is easier to set up than an Airflow pipeline but Airflow would increase scalablility.</p>

<p>The data storage layer uses a MongoDB client, this is simple and quick to set up, it allows querying of nested data, and doesn't require a pre-specified schema. In a production environment something like PostgreSQL would give better perfomance for large amounts of data.</p>

### How to use

1. Clone this repository.
2. Build the docker image

`docker-compose build`

3. Run the pipeline.

`docker-compose up`



### Issues

- DVC is not the best choice for this. Airflow scales better as it can run in a Kubernetes cluster.
- MongoDB is not the most performant database out there.
- The MongoDB state is not currently being persisted outside of the container.
- The security for the DB is still set to default.