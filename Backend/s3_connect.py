import boto3  # S3 Server connection
def s3_connection(): # S3 Server Configuration + Connection
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name = "ap-northeast-2", # 버킷 region
            aws_access_key_id = {}, #액세스 키 ID
            aws_secret_access_key = {}, #비밀 액세스 키
        )
    except Exception as e:
        print(e)
    else:
        print("S3 Bucket Connected!")
        return s3
    
def s3_put_object(s3, bucket, filepath, access_key): # (S3 <- Server) Upload Pic
    """
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치 - 올릴 파일
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    """
    try:
        s3.upload_file(
            Filename=filepath, # 업로드할 파일 경로
            Bucket=bucket,
            Key=access_key, # 업로드할 파일의 S3 내 위치와 이름을 나타낸다.
            ExtraArgs={"ContentType": "image/jpg", "ACL": "public-read"},
            # ContentType 파일 형식 jpg로 설정
            # ACL: 파일에 대한 접근 권한 설정
            # public-read, private, public-read-write, authenticated-read
        )
    except Exception as e:
        return False
    return True

def s3_get_image_url(s3, filename): # (S3 -> Server) Download Pic
    """
    s3 : 연결된 s3 객체(boto3 client)
    filename : s3에 저장된 파일 명
    """
    location = s3.get_bucket_location(Bucket={" 설정한 버킷 이름"})["LocationConstraint"]
    return f"https://{{설정한 버킷 이름}}.s3.{location}.amazonaws.com/{filename}.jpg"