<?php
/**
 * Plugin Name: Simplify Checkout for free items
 * Plugin URI: https://www.skyverge.com/blog/how-to-simplify-free-woocommerce-checkout/
 * Description: Removes field from checkout form
 * Author: SkyVerge
 * Author URI: https://www.skyverge.com/
 * Version: 1.0
 * Text Domain: skyverge-shortcodes
 *
 * Copyright: (c) 2014 SkyVerge, Inc. (spam@skyverge.com)
 *
 * License: GNU General Public License v3.0
 * License URI: http://www.gnu.org/licenses/gpl-3.0.html
 *
 * @author    SkyVerge
 * @copyright Copyright (c) 2014, SkyVerge, Inc.
 * @license   http://www.gnu.org/licenses/gpl-3.0.html GNU General Public License v3.0
 */

defined( 'ABSPATH' ) or exit;

/**
 * Removes coupon form, order notes, and several billing fields if the checkout doesn't require payment
 */
function sv_free_checkout_fields() {
    // Bail we're not at checkout, or if we're at checkout but payment is needed
    // Updated for ajax according to <https://stackoverflow.com/a/52089144>.
    if ( function_exists( 'is_checkout' ) && ( ! ( is_checkout() || is_ajax() ) || ( ( is_checkout() || is_ajax() ) && WC()->cart->needs_payment() ) ) ) {
        return;
    }

    // remove coupon forms since why would you want a coupon for a free cart??
    remove_action( 'woocommerce_before_checkout_form', 'woocommerce_checkout_coupon_form', 10 );

    // Remove the "Additional Info" order notes
    add_filter( 'woocommerce_enable_order_notes_field', '__return_false' );

    // Unset the fields we don't want in a free checkout
    function unset_unwanted_checkout_fields( $fields ) {
        // add or remove billing fields you do not want
        // list of fields: http://docs.woothemes.com/document/tutorial-customising-checkout-fields-using-actions-and-filters/#section-2
        $billing_keys = array(
            'billing_company',
            'billing_phone',
            'billing_address_1',
            'billing_address_2',
            'billing_city',
            'billing_postcode',
            'billing_country',
            'billing_state',
        );

        // unset each of those unwanted fields
        foreach( $billing_keys as $key ) {
            unset( $fields['billing'][$key] );
        }

        return $fields;
    }
    add_filter( 'woocommerce_checkout_fields', 'unset_unwanted_checkout_fields' );

    // A tiny CSS tweak for the account fields; this is optional
    function print_custom_css() {
        echo '<style>.create-account { margin-top: 6em; }</style>';
    }
    add_action( 'wp_head', 'print_custom_css' );
}

add_action( 'wp', 'sv_free_checkout_fields' );
