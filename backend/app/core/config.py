from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="GEOINT_")

    app_name: str = "Geospatial Intelligence Tracker API"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    opensky_url: str = "https://opensky-network.org/api/states/all"
    mapbox_style_url: str = "mapbox://styles/mapbox/dark-v11"
    cesium_ion_token: str = ""


settings = Settings()
