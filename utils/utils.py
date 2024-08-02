import math

class Utils:

    @staticmethod
    def convert_size(bytes):
        """
        Converts size given in `bytes` to best fitting unit of measure.
        """
        size_name = ("B", "KB", "MB", "GB", "TB")
        try:
            i = int(math.floor(math.log(bytes, 1024)))
            p = math.pow(1024, i)
            s = round(bytes / p, 2)
            return f"{s} {size_name[i]}"
        except ValueError:
            return "0 bits"
