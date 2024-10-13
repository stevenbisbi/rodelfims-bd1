FROM python:3.11-slim

WORKDIR /app

# Instalar las dependencias necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && apt-get clean

COPY .nixpacks/nixpkgs-bf446f08bff6814b569265bef8374cfdd3d8f0e0.nix .nixpacks/nixpkgs-bf446f08bff6814b569265bef8374cfdd3d8f0e0.nix
RUN nix-env -if .nixpacks/nixpkgs-bf446f08bff6814b569265bef8374cfdd3d8f0e0.nix && nix-collect-garbage -d

COPY . /app/.

RUN --mount=type=cache,id=s/6c97f769-12ef-45df-a107-c1d080bd0bdf-/root/cache/pip,target=/root/.cache/pip python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
