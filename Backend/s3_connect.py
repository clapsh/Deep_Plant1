import boto3  # S3 Server connection
import keyId  # Key 저장
import os

IMAGE_FOLDER_PATH = "./images/"


class S3Bucket:
    def __init__(self, folder):
        self.bucket = keyId.s3_bucket_name  # 버킷 지정
        self.folder = folder  # 저장할 폴더 지정
        try:
            self.s3 = boto3.client(
                service_name="s3",
                region_name="ap-northeast-2",  # 버킷 region
                aws_access_key_id=keyId.aws_access_key_id,  # 액세스 키 ID
                aws_secret_access_key=keyId.aws_secret_access_key,  # 비밀 액세스 키
            )
        except Exception as e:
            print(e)
        else:
            print("S3 Bucket Connected!")

    def transferImageData(self):  # flask server -> S3 Database
        for filename in os.listdir(IMAGE_FOLDER_PATH):
            if filename.endswith(".png"):
                filepath = os.path.join(IMAGE_FOLDER_PATH, filename)
                if self.put_object(self.bucket, filepath, f"{self.folder}/{filename}"):
                    print(
                        f"Successfully uploaded {filename} to {self.bucket}/{self.folder}"
                    )
                    os.remove(filepath)
                    print(f"Successfully removed {filename} from local disk")
                else:
                    print(f"Failed to upload {filename} to {self.bucket}/{self.folder}")

    def put_object(self, bucket, filepath, access_key):  # (S3 <- Server) Upload Pic
        """
        s3 bucket에 지정 파일 업로드
        :param bucket: 버킷명
        :param filepath: 파일 위치 - 올릴 파일
        :param access_key: 저장 파일명
        :return: 성공 시 True, 실패 시 False 반환
        """
        try:
            self.s3.upload_file(
                Filename=filepath,  # 업로드할 파일 경로
                Bucket=bucket,
                Key=access_key,  # 업로드할 파일의 S3 내 위치와 이름을 나타낸다.
                ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
                # ContentType 파일 형식 jpg로 설정
                # ACL: 파일에 대한 접근 권한 설정
                # public-read, private, public-read-write, authenticated-read
            )
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
        return True

    def get_image_url(self, bucket, filename):  # (S3 -> Server) Download Pic
        """
        :param bucket: 연결된 버킷명
        :param filename: s3에 저장된 파일 명
        """
        location = self.s3.get_bucket_location(Bucket=bucket)["LocationConstraint"]
        return f"https://{bucket}.s3.{location}.amazonaws.com/{filename}.jpg"
