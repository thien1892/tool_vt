# Tool-vt

Deploy in Google Cloud:

```bash
# Clone code
git clone git@github.com:thien1892/tool_vt.git tool-vt-2
cd tool-vt-2/

git clone -b vt https://github.com/thien1892/tool_vt.git

# Create a repo artifact
gcloud artifacts repositories create vt-tool-docker2 --repository-format=docker     --location=asia-east1 --description="Docker repository"
#  build container to artifact
gcloud builds submit --region=asia-east1 --tag asia-east1-docker.pkg.dev/tool-vt/vt-tool-docker2/vt-tool-docker2:tag1
# use cloud run to deploy port:8501 (streamlit)

```