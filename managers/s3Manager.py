import os
import sys

import aiofiles
from aiobotocore import session
from botocore.exceptions import BotoCoreError, ClientError
from sanic.log import logger

from utils.env import CONFIG
from utils.helpers import delete_local_temporary_files


class S3Manager:
    @classmethod
    async def generate_presigned_url_post(
        cls, key: str, content_type: str, config: dict
    ) -> dict:
        """
        This function is used to generate presigned url for uploading
        the logo on S3_Bucket.

        Args:
            key: name of file to be uploaded.
            content_type: type of content to be uploaded.
            config: dict of AWS to get bucket_name and region_name.


        Returns:
            Dict having presignedurl and fields.

        Raises:
            BadRequestException: This error is raised when we failed to
            generate presigned url.

        """

        region_name = config.get("S3_REGION")
        bucket_name = config.get("S3_BUCKET")

        session_object = session.get_session()

        fields = {
            "Content-Type": content_type,
            "success_action_status": "201",
        }

        conditions = [
            {"Content-Type": content_type},
            {"success_action_status": "201"},
        ]

        try:
            async with session_object.create_client(
                "s3", region_name=region_name
            ) as client:
                presigned_url = await client.generate_presigned_post(
                    bucket_name,
                    key,
                    fields,
                    conditions,
                )
        except BadRequestException:
            raise BadRequestException(ErrorMessages.PRESIGNED_URL_ERROR.value)

        return presigned_url

    @classmethod
    async def generate_presigned_url_get(cls, s3_url, s3_identifier, expires_in=3600):

        """
        This function takes the s3_url and generates a presigned_url
        for content to be publicly accessible.

        Args:
            s3_url: s3_url of file.
            expires_in: expiry time for presigned_url.
            s3_identifier: Identifier for bucket name

        Returns:
            presigned_url

        Raises:
            Badrequestexception: when failed to generate presigned_url.
        """
        config = CONFIG.config["AWS"][f"{s3_identifier}"]
        bucket_name = config.get("S3_BUCKET")
        region_name = config.get("S3_REGION")
        s3_host = f"https://{bucket_name}.s3.amazonaws.com/"
        key = s3_url.split(s3_host)[-1]
        session_object = session.get_session()
        try:
            async with session_object.create_client(
                    "s3", region_name=region_name
            ) as client:
                url = await client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name, "Key": key},
                    ExpiresIn=expires_in,
                )
        except BadRequestException:
            logger.debug(f"unable to convert in presigned url: {s3_url}")
            url = s3_url

        return url

    @classmethod
    async def get_file_from_s3(
            cls, key: str, s3_identifier: str, local_directory_path: str
    ):
        """
        This function is used to get content of a file from S3
        and store it in a new file in local storage.

        Args:
            s3_identifier: used to fetch bucket details from config
            key: S3 file object key, this key will also be
            used as filename in the local storage
            local_directory_path: local path where file will be stored

        Returns: Newly created filepath from local storage.
        """
        config = CONFIG.config["AWS"].get(s3_identifier, {})
        region_name = config.get("S3_REGION")
        bucket_name = config.get("S3_BUCKET")
        s3_key_prefix = config.get("S3_ORIGINAL_KEY_PREFIX", "")
        session_object = session.get_session()
        try:
            async with session_object.create_client(
                "s3", region_name=region_name
            ) as client:
                response = await client.get_object(Bucket=bucket_name, Key=key)
                async with response["Body"] as stream:
                    downloaded_bytes = await stream.read()
                    write_directory = f"{local_directory_path}/"
                    os.makedirs(write_directory, exist_ok=True)
                    if s3_key_prefix in key:
                        key = key.split(f"{s3_key_prefix}/")[-1]
                    filepath = f"{write_directory}{key}"
                    async with aiofiles.open(filepath, "wb") as file:
                        await file.write(downloaded_bytes)

        except BotoCoreError as ex:
            logger.exception(
                f"Exception occured while processing key {key} at "
                f"function get_file_from_s3: {ex}"
            )
            return ""

        return filepath

    @classmethod
    async def upload_file_on_s3(
        cls,
        key: str,
        filepath: str,
        s3_identifier: str,
    ) -> dict:
        """
        This function is used to upload file on S3.

        Args:
            key: S3 key
            filepath: local file path
            s3_identifier: identifier to fetch bucket details from config

        Returns: Response of put_object

        """
        config = CONFIG.config["AWS"].get(s3_identifier, {})
        region_name = config.get("S3_REGION")
        bucket_name = config.get("S3_BUCKET")
        session_object = session.get_session()
        try:
            async with aiofiles.open(filepath, "rb") as file:
                body = await file.read()
            async with session_object.create_client(
                "s3", region_name=region_name
            ) as client:
                response = await client.put_object(
                    Bucket=bucket_name, Key=key, Body=body
                )

        except BotoCoreError as ex:
            logger.exception(
                f"Exception occured while processing file {filepath} at {sys._getframe( ).f_code.co_name}: {ex}"
            )
            return {}

        return response

    @staticmethod
    def get_key_from_s3url(s3_url: str, s3_identifier: str) -> str:
        """
        This function fetches key from the provided s3 url.

        Args:
            s3_url: S3 url of file object
            s3_identifier: identifier to fetch bucket details from config

        Returns: key

        """
        config = CONFIG.config["AWS"].get(s3_identifier, {})
        bucket_name = config.get("S3_BUCKET")
        s3_host = f"https://{bucket_name}.s3.amazonaws.com/"
        key = s3_url.split(s3_host)[1]
        return key


    @classmethod
    async def get_file_from_s3_generic(
        cls, key, s3_identifier: str, local_directory_path: str
    ) -> str:
        """
        This function is used to get content of a file from S3
        and store it in a new file in local storage.

        Args:
            s3_identifier: used to fetch bucket details from config
            key: S3 file object key, this key will also be
            used as filename in the local storage
            local_directory_path: local filepath to write file

        Returns:
            Newly created filepath from local storage.
        """
        config = CONFIG.config["AWS"].get(s3_identifier, {})
        region_name = config.get("S3_REGION")
        bucket_name = config.get("S3_BUCKET")
        session_object = session.get_session()
        try:
            async with session_object.create_client(
                "s3", region_name=region_name
            ) as client:
                response = await client.get_object(Bucket=bucket_name, Key=key)
                async with response["Body"] as stream:
                    downloaded_bytes = await stream.read()
                    os.makedirs(local_directory_path, exist_ok=True)
                    file_name = key.split("/")[-1]
                    filepath = f"{local_directory_path}{file_name}"
                    async with aiofiles.open(filepath, "wb") as file:
                        await file.write(downloaded_bytes)
        except (BotoCoreError, ClientError) as ex:
            logger.exception(
                f"exception occurred while processing key {key} at "
                f"{sys._getframe().f_code.co_name}: {ex}"
            )
            return ""
        return filepath

    @classmethod
    async def get_object_header_from_s3url(
            cls, csv_url: str
    ) -> list:
        """
        This function is used to get headers of a file from S3

        Args:
            csv_url:S3 url of file object
        Returns:
            list of header
        """
        filepath = ""
        try:
            object_key = cls.get_key_from_s3url(csv_url, "S3_CSV")
            local_directory_path = f"{os.getcwd()}/temp/original_csv"
            filepath = await S3Manager.get_file_from_s3_generic(
                object_key, "S3_CSV", local_directory_path
            )
            if not filepath:
                raise BadRequestException(
                    "No such key found"
                )
            parser = CSVParser(
                filepath=filepath,
            )
            header = parser.create_header()
        except FileNotFoundError as ex:
            logger.exception(
                f"exception occurred while fetching headers {ex}"
            )
            return []
        finally:
            await delete_local_temporary_files(filepath)
        return header
