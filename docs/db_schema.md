account.EmailAddress
    Fields:
        emailconfirmation -
        id -
        user -
        email -
        verified -
        primary -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        can_set_verified()
        get_constraints()
        remove()
        send_confirmation()
        set_as_primary()
        set_verified()
        validate_constraints()

account.EmailConfirmation
    Fields:
        id -
        email_address -
        created -
        sent -
        key -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        confirm()
        create()
        from_key()
        get_constraints()
        get_next_by_created()
        get_previous_by_created()
        key_expired()
        send()
        validate_constraints()

accounts.Company
    Fields:
        stores -
        letterheads -
        number -
        created -
        updated -
        tax_number -
        address -
        postal_code -
        city -
        country -
        street -
        name -
        handle -
        description -
        user -
        code -
        ar_name -
        logo -
        is_default -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_create_url()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        get_update_url()
        has_stores()
        items()
        validate_constraints()

accounts.Country
    Fields:
        theme -
        id -
        user -
        name -
        code -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

accounts.Customer
    Fields:
        discounts -
        documents -
        customer_loyalty_cards -
        orders -
        stock_controls -
        id -
        user -
        code -
        slug -
        name -
        address -
        postal_code -
        city -
        tax_number -
        email -
        phone -
        is_enabled -
        is_customer -
        is_supplier -
        due_date_period -
        image -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        generate_code()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        refresh_cache()
        validate_constraints()

accounts.CustomerDiscount
    Fields:
        id -
        user -
        customer -
        type -
        uid -
        value -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

accounts.Employee
    Fields:
        id -
        user -
        full_name -
        position -
        is_active -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

accounts.Logo
    Fields:
        company -
        store -
        number -
        created -
        updated -
        name -
        image -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

accounts.Region
    Fields:
        theme -
        id -
        name -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

accounts.SecurityKey
    Fields:
        access_level -
        user -
        name -
        level -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

accounts.Store
    Fields:
        number -
        created -
        updated -
        tax_number -
        address -
        postal_code -
        city -
        country -
        street -
        name -
        handle -
        description -
        user -
        code -
        company -
        logo -
        is_default -
        hashed_license -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_create_url()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        get_update_url()
        has_items()
        has_stores()
        items()
        licence_veryfy()
        user_has_items()
        validate_constraints()

accounts.User
    Fields:
        logentry -
        emailaddress -
        employee -
        customers -
        customer_discounts -
        companies -
        stores -
        warehouses -
        countries -
        security_keys -
        country -
        documents -
        document_items -
        document_categories -
        document_types -
        document_item_taxes -
        payments -
        payment_types -
        fiscals -
        customer_loyalty_cards -
        floor_plans -
        floor_plan_tables -
        barcodes -
        currencies -
        productGroups -
        products -
        comments -
        orders -
        order_items -
        order_statuses -
        Pos_printer_selections -
        pos_printer_selection_settings -
        pos_printer_settings -
        product_group_print_stations -
        product_print_stations -
        company_letterheads -
        company_letterhead_options -
        taxes -
        productTaxes -
        stocks -
        stock_controls -
        id -
        password -
        last_login -
        is_superuser -
        access_level -
        email -
        name -
        image -
        pin -
        is_active -
        is_staff -
        created -
        updated -
        groups -
        user_permissions -
    Methods (non-private/internal):
        acheck_password()
        adelete()
        aget_all_permissions()
        aget_group_permissions()
        aget_user_permissions()
        ahas_module_perms()
        ahas_perm()
        ahas_perms()
        arefresh_from_db()
        asave()
        check_password()
        get_all_permissions()
        get_constraints()
        get_email_field_name()
        get_group_permissions()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        get_session_auth_fallback_hash()
        get_session_auth_hash()
        get_user_permissions()
        get_username()
        has_module_perms()
        has_perm()
        has_perms()
        has_usable_password()
        natural_key()
        normalize_username()
        set_password()
        set_unusable_password()
        validate_constraints()

accounts.Warehouse
    Fields:
        documents -
        document_types -
        orders -
        stocks -
        id -
        user -
        name -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

admin.LogEntry
    Fields:
        id -
        action_time -
        user -
        content_type -
        object_id -
        object_repr -
        action_flag -
        change_message -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_action_flag_display()
        get_admin_url()
        get_change_message()
        get_constraints()
        get_edited_object()
        get_next_by_action_time()
        get_previous_by_action_time()
        is_addition()
        is_change()
        is_deletion()
        validate_constraints()

auth.Group
    Fields:
        user -
        id -
        name -
        permissions -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        natural_key()
        validate_constraints()

auth.Permission
    Fields:
        group -
        user -
        id -
        name -
        content_type -
        codename -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        natural_key()
        validate_constraints()

configurations.AppTable
    Fields:
        apptablecolumn -
        id -
        name -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

configurations.AppTableColumn
    Fields:
        id -
        app -
        name -
        title -
        is_enabled -
        is_related -
        related_value -
        searchable -
        orderable -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

configurations.ApplicationProperty
    Fields:
        id -
        user -
        section -
        name -
        value -
        title -
        description -
        input_type -
        editable -
        order -
        params -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_input_type_display()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

configurations.ApplicationPropertySection
    Fields:
        children -
        application_properties -
        id -
        parent -
        name -
        icon -
        description -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

configurations.Counter
    Fields:
        id -
        user -
        name -
        value -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

configurations.Migration
    Fields:
        id -
        version -
        description -
        file_name -
        module -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

contenttypes.ContentType
    Fields:
        logentry -
        permission -
        id -
        app_label -
        model -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_all_objects_for_this_type()
        get_constraints()
        get_object_for_this_type()
        model_class()
        natural_key()
        validate_constraints()

documents.Document
    Fields:
        document_items -
        payments -
        id -
        number -
        user -
        customer -
        cash_register -
        order -
        document_type -
        warehouse -
        date -
        reference_document_number -
        internal_note -
        note -
        due_date -
        discount -
        discount_type -
        discount_apply_rule -
        paid_status -
        stock_date -
        total -
        is_clocked_out -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_date()
        get_next_by_due_date()
        get_next_by_stock_date()
        get_next_by_updated()
        get_paid_status_display()
        get_previous_by_created()
        get_previous_by_date()
        get_previous_by_due_date()
        get_previous_by_stock_date()
        get_previous_by_updated()
        validate_constraints()

documents.DocumentCategory
    Fields:
        document_types -
        id -
        user -
        name -
        language -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

documents.DocumentItem
    Fields:
        number -
        user -
        document -
        product -
        expected_quantity -
        quantity -
        price -
        discount -
        discount_type -
        discount_apply_rule -
        returned -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

documents.DocumentItemTax
    Fields:
        id -
        user -
        tax -
        amount -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

documents.DocumentType
    Fields:
        documents -
        orders -
        id -
        user -
        name -
        code -
        category -
        warehouse -
        stock_direction -
        editor_type -
        print_template -
        price_type -
        language -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

finances.AssetClass
    Fields:
        theme -
        id -
        name -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

finances.FiscalItem
    Fields:
        id -
        user -
        plu -
        name -
        vat -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

finances.Fund
    Fields:
        themes -
        fundvalue -
        id -
        name -
        market_summary -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

finances.FundValue
    Fields:
        id -
        fund -
        date -
        value -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_date()
        get_previous_by_date()
        validate_constraints()

finances.IndexValue
    Fields:
        id -
        date -
        value -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_date()
        get_previous_by_date()
        validate_constraints()

finances.Payment
    Fields:
        id -
        user -
        document -
        payment_type -
        amount -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

finances.PaymentType
    Fields:
        payments -
        id -
        user -
        name -
        code -
        is_customer_required -
        is_fiscal -
        is_slip_required -
        is_change_allowed -
        ordinal -
        is_enabled -
        is_quick_payment -
        open_cash_drawer -
        shortcut -
        mark_as_paid -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        update_tree_nodes()
        validate_constraints()

finances.Position
    Fields:
        id -
        theme -
        var -
        cvar -
        LTD -
        SL -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

finances.Rationale
    Fields:
        id -
        theme -
        action -
        rationale -
        date -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_date()
        get_previous_by_date()
        validate_constraints()

finances.Theme
    Fields:
        position -
        rationale -
        id -
        name -
        target_PL -
        fund -
        region -
        country -
        asset_class -
        live -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

orders.PosOrder
    Fields:
        items -
        number -
        user -
        customer -
        item_subtotal -
        document_type -
        warehouse -
        date -
        reference_document_number -
        internal_note -
        note -
        due_date -
        discount -
        discount_type -
        discounted_amount -
        discount_sign -
        subtotal_after_discount -
        fixed_taxes -
        total_tax_rate -
        total_tax -
        total -
        paid_status -
        status -
        is_active -
        is_enabled -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_date()
        get_next_by_due_date()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_date()
        get_previous_by_due_date()
        get_previous_by_updated()
        get_status_class()
        refresh_cache()
        set_tax_fields()
        validate_constraints()

orders.PosOrderItem
    Fields:
        number -
        user -
        order -
        product -
        round_number -
        quantity -
        price -
        is_locked -
        is_enabled -
        is_active -
        discount -
        discount_type -
        discounted_amount -
        discount_sign -
        item_total_before_discount -
        item_total -
        is_featured -
        voided_by -
        comment -
        bundle -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

orders.PosOrderStatus
    Fields:
        posorder -
        id -
        user -
        name -
        ordinal -
        color_class -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_color_class_display()
        get_constraints()
        validate_constraints()

pos.CashRegister
    Fields:
        documents -
        Pos_printer_selections -
        number -
        name -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

pos.FloorPlan
    Fields:
        tables -
        id -
        user -
        name -
        color -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

pos.FloorPlanTable
    Fields:
        id -
        user -
        name -
        floor_plan -
        position_x -
        position_y -
        width -
        height -
        is_round -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

pos.LoyaltyCard
    Fields:
        id -
        user -
        customer -
        number -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.CompanyLetterhead
    Fields:
        id -
        user -
        company -
        name -
        letterhead_options -
        is_default -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.CompanyLetterheadOption
    Fields:
        options -
        id -
        user -
        name -
        paper_format -
        paper_width -
        paper_height -
        top_margin -
        bottom_margin -
        left_margin -
        right_margin -
        inner_width -
        inner_height -
        unicode_font -
        unicode_text_header_size -
        text_header_size -
        unicode_text_content_size -
        text_content_size -
        table_text_content_size -
        font_family -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_measures()
        get_next_by_created()
        get_next_by_updated()
        get_paper_format_display()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.PosPrinterSelection
    Fields:
        pos_printer_selection_settings -
        printstationposprinterselection -
        id -
        user -
        key -
        cash_register -
        printer_name -
        is_enabled -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.PosPrinterSelectionSettings
    Fields:
        id -
        user -
        pos_printer_selection -
        paper_width -
        header -
        footer -
        feed_lines -
        cut_paper -
        print_bitmap -
        open_cash_drawer -
        cash_drawer_command -
        header_alignment -
        footer_alignment -
        is_formatting_enabled -
        printer_type -
        number_of_copies -
        code_page -
        character_set -
        margin -
        left_margin -
        top_margin -
        right_margin -
        bottom_margin -
        print_barcode -
        font_name -
        font_size_percent -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.PosPrinterSettings
    Fields:
        id -
        user -
        printer_name -
        paper_width -
        header -
        footer -
        feed_lines -
        cut_paper -
        print_bitmap -
        open_cash_drawer -
        cash_drawer_command -
        header_alignment -
        footer_alignment -
        is_formatting_enabled -
        printer_type -
        number_of_copies -
        code_page -
        character_set -
        margin -
        left_margin -
        top_margin -
        right_margin -
        bottom_margin -
        print_barcode -
        font_name -
        font_size_percent -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.PrintStation
    Fields:
        printstationposprinterselection -
        product_group_print_stations -
        product_print_stations -
        id -
        name -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

printers.PrintStationPosPrinterSelection
    Fields:
        id -
        print_station -
        pos_printer_selection -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

printers.ProductGroupPrintStation
    Fields:
        id -
        user -
        product_group -
        print_station -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

printers.ProductPrintStation
    Fields:
        id -
        user -
        product -
        print_station -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

products.Barcode
    Fields:
        id -
        user -
        product -
        value -
        image -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

products.Currency
    Fields:
        products -
        id -
        user -
        name -
        code -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

products.Product
    Fields:
        document_items -
        barcode -
        comments -
        order_items -
        product_print_stations -
        productTaxes -
        stocks -
        stock_controls -
        id -
        user -
        name -
        slug -
        parent_group -
        country_of_origin -
        code -
        description -
        plu -
        measurement_unit -
        price -
        currency -
        is_tax_inclusive_price -
        is_price_change_allowed -
        is_service -
        is_using_default_quantity -
        is_product -
        cost -
        margin -
        image -
        color -
        is_enabled -
        age_restriction -
        last_purchase_price -
        rank -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_annotations_fields()
        get_columns()
        get_constraints()
        get_country_of_origin_display()
        get_fields()
        get_indexes()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        get_related_fields()
        img()
        validate_constraints()

products.ProductComment
    Fields:
        id -
        user -
        product -
        comment -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

products.ProductGroup
    Fields:
        groups -
        products -
        product_group_print_stations -
        id -
        user -
        name -
        slug -
        parent -
        color -
        image -
        rank -
        is_product -
        is_enabled -
        created -
        updated -
        lft -
        rght -
        tree_id -
        level -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_ancestors()
        get_children()
        get_constraints()
        get_descendant_count()
        get_descendants()
        get_family()
        get_leafnodes()
        get_level()
        get_next_by_created()
        get_next_by_updated()
        get_next_sibling()
        get_previous_by_created()
        get_previous_by_updated()
        get_previous_sibling()
        get_root()
        get_siblings()
        insert_at()
        is_ancestor_of()
        is_child_node()
        is_descendant_of()
        is_leaf_node()
        is_root_node()
        move_to()
        validate_constraints()

sessions.Session
    Fields:
        session_key -
        session_data -
        expire_date -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_decoded()
        get_next_by_expire_date()
        get_previous_by_expire_date()
        get_session_store_class()
        validate_constraints()

sites.Site
    Fields:
        id -
        domain -
        name -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        natural_key()
        validate_constraints()

stock.Stock
    Fields:
        id -
        user -
        product -
        warehouse -
        quantity -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        refresh_cache()
        validate_constraints()

stock.StockControl
    Fields:
        id -
        user -
        product -
        customer -
        reorder_point -
        preferred_quantity -
        is_low_stock_warning_enabled -
        low_stock_warning_quantity -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        validate_constraints()

tax.ProductTax
    Fields:
        id -
        user -
        product -
        tax -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()

tax.Tax
    Fields:
        document_item_taxes -
        productTaxes -
        id -
        user -
        name -
        rate -
        code -
        is_fixed -
        is_tax_on_total -
        is_enabled -
        amount -
        created -
        updated -
    Methods (non-private/internal):
        adelete()
        arefresh_from_db()
        asave()
        get_constraints()
        get_next_by_created()
        get_next_by_updated()
        get_previous_by_created()
        get_previous_by_updated()
        validate_constraints()
