page_result_path_map: {str: str} = {}
page_html_result_path_map: {str: str} = {}
page_json_result_path_map: {str: str} = {}
page_utf_result_path_map: {str: str} = {}
page_resource_result_path_map: {str: str} = {}


class PageDealerContext:
   @staticmethod
   def get_result_path_map() -> {str: str}:
       return page_result_path_map

   @staticmethod
   def get_html_result_path_map() -> {str: str}:
       return page_html_result_path_map

   @staticmethod
   def get_json_result_path_map() -> {str: str}:
       return page_json_result_path_map

   @staticmethod
   def get_utf_result_path_map() -> {str: str}:
       return page_utf_result_path_map

   @staticmethod
   def get_resource_result_path_map() -> {str: str}:
       return page_resource_result_path_map