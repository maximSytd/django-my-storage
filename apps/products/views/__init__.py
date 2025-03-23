from .category import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from .product import (
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
)
from .supplier import (
    SupplierCreateView,
    SupplierListView,
    SupplierUpdateView,
)
from .shipment import (
    ShipmentCreateView,
    ShipmentListView,
    ShipmentDetailView,
    ShipmentUpdateView,
    ShipmentDeleteView,
)
from .product_activity import (
    ProductActivityDeleteView,
    ProductActivityUpdateView,
)
from .write_off import (
    WriteOffListView,
    WriteOffCreateView,
    WriteOffDetailView,
    WriteOffDeleteView,
)
from .departure_point import (
    DeparturePointCreateView,
)