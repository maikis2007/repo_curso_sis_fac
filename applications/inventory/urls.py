from django.urls import path
from django.urls.resolvers import URLPattern
from applications.inventory.views import *

app_name = "inventory"

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name="category_list"),
    path('new/category/', CategoryCreateView.as_view(), name="category_new"),
    path('edit/category/<int:id_category>', category_edit, name="category_edit"),
    path('delete/category/<int:id_category>', category_delete, name="category_delete"),
    path('edit/category/state/<int:id_category>', category_state, name="category_state"),

    path('subcategories/', subcategory_list, name="subcategory_list"),
    path('new/subcategory/', SubcategoryCreateView.as_view(), name="subcategory_new"),
    path('edit/subcategory/<int:id_subcategory>', subcategory_edit, name="subcategory_edit"),
    path('delete/subcategory/<int:id_subcategory>', subcategory_delete, name="subcategory_delete"),
    path('edit/subcategory/state/<int:id_subcategory>', subcategory_state, name="subcategory_state"),

    path('marks/', MarkListView.as_view(), name="mark_list"),
    path('new/mark/', MarkCreateView.as_view(), name="mark_new"),
    path('edit/mark/<int:id_mark>', mark_edit, name="mark_edit"),
    path('delete/mark/<int:id_mark>', mark_delete, name="mark_delete"),
    path('edit/mark/state/<int:id_mark>', mark_state, name="mark_state"),

    path('units_measures/', UnitMeasureListView.as_view(), name="unit_measure_list"),
    path('new/unit_measure/', UnitMeasureCreateView.as_view(), name="unit_measure_new"),
    path('edit/unit_measure/<int:id_unit_measure>', unit_measure_edit, name="unit_measure_edit"),
    path('delete/unit_measure/<int:id_unit_measure>', unit_measure_delete, name="unit_measure_delete"),
    path('edit/unit_measure/state/<int:id_unit_measure>', unit_measure_state, name="unit_measure_state"),
]
