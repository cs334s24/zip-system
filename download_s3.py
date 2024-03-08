import os
import sh


# Download the sample data from S3
def download_from_s3(docket_id):
    os.mkdir("sample-data")
    docket_info = docket_id.split("-")
    sh.aws('s3', 'cp', 's3://mirrulations-sample-data-opensearch/' + docket_info[0] + '/' + docket_id, 'sample-data', '--recursive')

def main():
    if os.path.exists("sample-data"):
        sh.rm('-r', 'sample-data')
    download_from_s3("IHS-2005-0004")

if __name__ == "__main__":
    main()
