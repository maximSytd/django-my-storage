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
    SupplierDeleteView,
)
from .shipment import (
    ShipmentCreateView,
    ShipmentListView,
    ShipmentDetailView,
    ShipmentUpdateView,
    ShipmentDeleteView,
    ShipmentFollowView,
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
    DeparturePointListView,
    DeparturePointUpdateView,
    DeparturePointDeleteView,
)

from .summary import (
    DashboardSummaryView,
    ProductActivitySummaryView,
    SupplierSummaryView,
)

from .storage import (
    StorageCreateView,
    StorageUpdateView,
)