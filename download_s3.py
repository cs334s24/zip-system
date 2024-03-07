import os
import sh


# Download the sample data from S3
def download_from_s3():
    os.mkdir("sample-data")
    sh.aws('s3', 'cp', 's3://mirrulations-sample-data-opensearch', 'sample-data', '--recursive')


def main():
    if os.path.exists("sample-data"):
        sh.rm('-r', 'sample-data')
    download_from_s3()

if __name__ == "__main__":
    main()
