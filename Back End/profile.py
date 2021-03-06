import os
import images
import config
import PIL.Image
import files
import errors
from database import request_utils, mysql_connection


class Profile:
    """
    Profile of a user.
    """

    def __init__(self, user=None, id: int = None):
        """
        Init for the profile class.
        :param user: User whose profile this class need to be.
        :type user: user.User
        :param id: Id of this user's profile.

        There is two different ways of initializing this profile.
            - Through a user object. This gives access to all of this class functionality (modifying
            profile data and getting profile data).
            - Through a user's id. This only allows to retrieve profile information.
        """
        self.user = user
        if user:
            self.cursor = user.cursor
        else:
            self.cursor = mysql_connection.cnx.cursor(dictionary=True)

        if user:
            self.id = user.id
        else:
            self.id = id

    @property
    def use_default_image(self) -> bool:
        query = f"""SELECT use_default_picture FROM UserTable WHERE id = {self.id};"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0]["use_default_picture"]
        return result

    @property
    def profile_picture_directory(self) -> str:
        """
        Path leading to the profile_picture_directory where user's profile picture images are stored.
        :return:
        """
        return f'Medias/profile_picture/{self.id}'

    @property
    def default_profile_picture(self) -> bytes:
        with open("default_avatar.png", 'rb') as f:
            return f.read()

    @property
    def profile_picture(self) -> bytes:
        try:
            if self.use_default_image:
                return self.default_profile_picture
            else:
                with open(os.path.join(self.profile_picture_directory, "picture.png"), 'rb') as f:
                    return f.read()
        except Exception as e:
            raise errors.UserNotExisting

    @property
    def profile_picture_api_route(self) -> str:
        return f"/user/{self.id}/profile/picture"

    def update(self, caption: str = None, profile_picture: PIL.Image = None, public_visibility: bool = None,
               username: str = None, name: str = None):
        """
        Update this profile values. All arguments are optional, if they are not provided the value stay as it is.
        :param caption:
        :param profile_picture:
        :param public_visibility:
        :return:
        """
        if not (caption or profile_picture or public_visibility or name or username):
            # No data is to be changed, every argument is set to None.
            return

        if username and request_utils.value_in_database("UserTable", "username", username):
            raise errors.UsernameTaken

        profile_picture_path = None
        if profile_picture:
            picture = images.resize_image(image=profile_picture, length=config.PROFILE_PICTURE_DIMENSION)

            picture.filename = f"picture.png"

            profile_picture_path = os.path.join(self.profile_picture_directory, picture.filename)
            files.prepare_directory(self.profile_picture_directory)
            picture.save(profile_picture_path)

        update_query = """
        UPDATE UserTable SET """
        if caption:
            update_query += f"""caption = "{caption}","""
        if public_visibility:
            if str(public_visibility).lower() == "false" or str(public_visibility).lower() == "true":
                update_query += f"""public_profile = {public_visibility},"""
        if profile_picture_path:
            update_query += f"""use_default_picture = FALSE,"""
        if name:
            update_query += f"""name = "{name}","""
        if username:
            update_query += f"""username = "{username}","""

        update_query = update_query[:-1]  # Removes the coma ","

        update_query += f" WHERE id = {self.user.id};"
        self.cursor.execute(update_query)

    def get(self, token: str = None) -> dict:
        """
        Get the profile data for a user.
        :param token: Token of the user asking for the profile data. This is optional. It may be provided to allow the
        retrieval of data only available if the user is followed. In case of a private account only followers can access
        the number of posts.
        :return: Profile data in a dictionary :
            caption : str
            name : str
            username : str
            public_profile : bool
            follower_num : int
            following_num : int
            profile_picture_api_path : str
        """
        profile_id = self.id
        if not profile_id:
            profile_id = self.user.id

        get_profile_data_query = f"""
        SELECT name, username, caption, public_profile, (SELECT COUNT(*) FROM Follow WHERE user_id_followed = id) AS follower, (SELECT COUNT(*) FROM Follow WHERE user_id = id) AS following FROM UserTable
        WHERE id = {profile_id};
        """
        self.cursor.execute(get_profile_data_query)
        results = self.cursor.fetchall()
        if len(results) != 1:
            raise errors.UserNotExisting(id=self.id)
        results = results[0]
        results["profile_picture_route"] = self.profile_picture_api_route
        return results
