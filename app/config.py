from pydantic_settings import SettingsConfigDict, BaseSettings


class SettingsLocal(BaseSettings):
    database_hostname: str
    # database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class SettingsAD(BaseSettings):
    database_hostname: str
    # database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env_AD", env_file_encoding="utf-8")

    # class Config:
    #     env_file = ".env"


settings_local = SettingsLocal()
settings_ad = SettingsAD()
