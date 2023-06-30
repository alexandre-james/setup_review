from openpype.tools.creator.model import CreatorsModel
from openpype.tools.creator.constants import ITEM_ID_ROLE
from openpype.pipeline.create import legacy_create
from openpype.pipeline import legacy_io
import maya.api.OpenMaya as om
import maya.cmds as cmds

def run():
    ### Get all cameras first ###
    cameras = cmds.ls(type=('camera'), l=True)

    ### Filter out main cameras ###
    main_cameras = [camera for camera in cameras if "cameraMain" in camera]

    if len(main_cameras) == 0:
        log("No main cameras found. Aborting.", type="error")
        return

    if len(main_cameras) > 1:
        log("Multiple main cameras found. Taking the first one.", type="warning")

    ### select main camera ###
    main_camera = main_cameras[0]
    cmds.select(main_camera)

    ### create review ###
    create_review()
    
    ### reset selection ###
    cmds.select(clear=True)

def create_review():
    ### get review creator ###
    creators_model = CreatorsModel()
    creators_model.reset()

    indexes = creators_model.get_indexes_by_family("review")

    if len(indexes) == 0:
        log("No review creator found. Aborting.", type="error")
        return

    index = indexes[0]
    item_id = index.data(ITEM_ID_ROLE)
    creator_plugin = creators_model.get_creator_by_id(item_id)

    ### get asset name ###
    asset_name = legacy_io.Session["AVALON_ASSET"]

    ### setup arguments ###
    subset_name = "reviewMain"
    use_selection = True
    variant = "Main"

    ### create review ###
    try:
        legacy_create(
            creator_plugin,
            subset_name,
            asset_name,
            options={"useSelection": use_selection},
            data={"variant": variant}
        )

    except Exception as e:
        log("Failed to create review instance. Aborting.", type="error")
        log(str(e), type="error")
        return

def log(msg, type="info"):
    if type == "info":
        om.MGlobal.displayInfo(msg)

    elif type == "warning":
        om.MGlobal.displayWarning(msg)

    elif type == "error":
        om.MGlobal.displayError(msg)