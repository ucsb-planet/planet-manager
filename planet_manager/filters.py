from planet.data_filter import (
    and_filter,
    range_filter,
    string_in_filter,
    permission_filter,
    asset_filter,
)


class Filters:
    base_filter = and_filter(
        [
            # geometry_filter(aoi),
            string_in_filter("instrument", ["PSB.SD", "PS2.SD", "PS2"]),
            range_filter("cloud_cover", lte=10),
            range_filter("clear_confidence_percent", gte=90),
            range_filter("gsd", lte=5),
            range_filter("visible_confidence_percent", gte=85),
            string_in_filter("ground_control", ["true"]),
            string_in_filter("quality_category", ["standard"]),
        ]
    )

    ps2_sd_4b = and_filter(
        [
            # string_in_filter("item_type", ["PSScene"]),
            string_in_filter("instrument", ["PS2.SD"]),
            range_filter("cloud_cover", lte=10),
            range_filter("clear_confidence_percent", gte=90),
            range_filter("gsd", lte=5),
            range_filter("visible_confidence_percent", gte=85),
            string_in_filter("quality_category", ["standard"]),
            string_in_filter("publishing_stage", ["finalized"]),
            asset_filter(
                [
                    "ortho_analytic_4b",
                    "ortho_analytic_4b_sr",
                    "ortho_analytic_4b_xml",
                    "ortho_udm2",
                ]
            ),
            # TODO: configure permission_filter
            permission_filter(),
            range_filter("view_angle", gte=0, lte=60),
            string_in_filter("ground_control", ["true"]),
        ]
    )

    ps2_4b = and_filter(
        [
            # string_in_filter("item_type", ["PSScene"]),
            string_in_filter("instrument", ["PS2"]),
            range_filter("cloud_cover", lte=10),
            range_filter("clear_confidence_percent", gte=90),
            range_filter("cloud_cover", lte=10),
            range_filter("clear_confidence_percent", gte=90),
            range_filter("gsd", lte=5),
            range_filter("visible_confidence_percent", gte=85),
            string_in_filter("quality_category", ["standard"]),
            string_in_filter("publishing_stage", ["finalized"]),
            asset_filter(
                [
                    "ortho_analytic_4b",
                    "ortho_analytic_4b_sr",
                    "ortho_analytic_4b_xml",
                    "ortho_udm2",
                ]
            ),
            # TODO: configure permission_filter
            permission_filter(),
            range_filter("view_angle", gte=0, lte=60),
            string_in_filter("ground_control", ["true"]),
        ]
    )

    psb_sd_8b = and_filter(
        [
            # string_in_filter("item_type", ["PSScene"]),
            string_in_filter("instrument", ["PSB.SD"]),
            range_filter("cloud_cover", lte=10),
            range_filter("clear_confidence_percent", gte=90),
            range_filter("gsd", lte=5),
            range_filter("visible_confidence_percent", gte=85),
            string_in_filter("quality_category", ["standard"]),
            string_in_filter("publishing_stage", ["finalized"]),
            asset_filter(
                [
                    "ortho_analytic_8b",
                    "ortho_analytic_8b_sr",
                    "ortho_analytic_8b_xml",
                    "ortho_udm2",
                ]
            ),
            # TODO: configure permission_filter
            permission_filter(),
            range_filter("view_angle", gte=0, lte=60),
            string_in_filter("ground_control", ["true"]),
        ]
    )
