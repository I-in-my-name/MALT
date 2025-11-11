
// Include I2S driver
#include "driver/i2s_std.h"
#include <stdio.h> // Required for file operations (FILE*)
#include <math.h>
#include "esp_timer.h"

// Connections to INMP441 I2S microphone
#define EXAMPLE_I2S_DUPLEX_MODE 1

#define EXAMPLE_STD_MCLK_IO1 19
#define EXAMPLE_STD_BCLK_IO1 19 // I2S bit clock io number
#define EXAMPLE_STD_WS_IO1 18   // I2S word select io number
#define OUT1 25                 // I2S data out io number
#define OUT2 25                 // I2S data out io number
#define IN1 32                  // I2S data in io number
#define IN2 33                  // I2S data in io number

#define EXAMPLE_BUFF_SIZE 2048

static i2s_chan_handle_t chan1; // I2S rx channel handler
static i2s_chan_handle_t chan2; // I2S rx channel handler
static i2s_chan_handle_t chan3; // I2S rx channel handler
static i2s_chan_handle_t chan4; // I2S rx channel handler

// Define input buffer length
#define bufferLen 64
int16_t sBuffer_ALPHA[bufferLen];
int16_t sBuffer_BETA[bufferLen];

// --- I2S Configuration Functions (No changes needed here) ---
/*
 * SPDX-FileCopyrightText: 2021-2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */

#include <stdint.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2s_std.h"
#include "driver/gpio.h"
#include "esp_check.h"
#include "sdkconfig.h"

// Note: MCLK is defined but is NOT used in the final configuration to resolve the GPIO conflict.
// If you intended to use MCLK, it MUST be on a different pin than BCLK (19).
#define EXAMPLE_I2S_DUPLEX_MODE 1

#define EXAMPLE_STD_MCLK_IO1 19
#define EXAMPLE_STD_BCLK_IO1 19 // I2S bit clock io number
#define EXAMPLE_STD_WS_IO1 18   // I2S word select io number
#define OUT1 14                 // I2S data out io number
#define EXAMPLE_STD_DIN_IO1 33  // I2S data in io number

#define EXAMPLE_BUFF_SIZE 2048

static i2s_chan_handle_t chan1; // I2S tx channel handler
static i2s_chan_handle_t chan2; // I2S tx channel handler
static i2s_chan_handle_t chan3; // I2S tx channel handler
static i2s_chan_handle_t chan4; // I2S tx channel handler

// --- Removed i2s_example_read_task() and merged logic into app_main ---

// --- FILE SAVING FUNCTION ---
// Assumes the filesystem (e.g., SPIFFS) has been initialized and mounted.
void save_first_stereo_sample(const uint8_t *i2s_buffer, int64_t timestamp)
{

    printf("%f,%u,%u,%u,%u,%u,%u\n", timestamp, i2s_buffer[1], i2s_buffer[2], i2s_buffer[3], i2s_buffer[5], i2s_buffer[6], i2s_buffer[7]);

    // uint8_t *relevant6 = (uint8_t *)calloc(6, 1);
    // relevant6[0] = i2s_buffer[1];
    // relevant6[1] = i2s_buffer[2];
    // relevant6[2] = i2s_buffer[3];
    // relevant6[3] = i2s_buffer[5];
    // relevant6[4] = i2s_buffer[6];
    // relevant6[5] = i2s_buffer[7];
}

static void i2s_example_init_std_duplex(void)
{
    /* Step 1: Determine the I2S channel configuration and allocate both channels */
    i2s_chan_config_t pair1 = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_AUTO, I2S_ROLE_MASTER);
    i2s_chan_config_t pair2 = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_AUTO, I2S_ROLE_SLAVE);
    ESP_ERROR_CHECK(i2s_new_channel(&pair1, NULL, &chan2));
    ESP_ERROR_CHECK(i2s_new_channel(&pair2, NULL, &chan4));

    /* Step 2: Setting the configurations of standard mode, and initialize rx & tx channels */
    i2s_std_config_t std_cfg1 = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
        .slot_cfg = {
            // Data width is 24 bits (the actual audio precision)
            .data_bit_width = I2S_DATA_BIT_WIDTH_24BIT,
            // Slot width is 32 bits (the size of the register slot used for DMA)
            .slot_bit_width = I2S_SLOT_BIT_WIDTH_32BIT,
            .slot_mode = I2S_SLOT_MODE_STEREO,
            .slot_mask = I2S_STD_SLOT_BOTH,
            .ws_width = 0, // Default
        },
        .gpio_cfg = {
            // FIX 1: MCLK was set to 19 (same as BCLK). Set to UNUSED.
            .mclk = I2S_GPIO_UNUSED,
            .bclk = EXAMPLE_STD_BCLK_IO1,
            .ws = EXAMPLE_STD_WS_IO1,
            .dout = OUT1, // NOT NEEDED !!
            // FIX 2: DIN was set to UNUSED. Use the defined DIN pin (33).
            .din = IN1,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    i2s_std_config_t std_cfg2 = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
        .slot_cfg = {
            // Data width is 24 bits (the actual audio precision)
            .data_bit_width = I2S_DATA_BIT_WIDTH_24BIT,
            // Slot width is 32 bits (the size of the register slot used for DMA)
            .slot_bit_width = I2S_SLOT_BIT_WIDTH_32BIT,
            .slot_mode = I2S_SLOT_MODE_STEREO,
            .slot_mask = I2S_STD_SLOT_BOTH,
            .ws_width = 0, // Default
        },
        .gpio_cfg = {
            // FIX 1: MCLK was set to 19 (same as BCLK). Set to UNUSED.
            .mclk = I2S_GPIO_UNUSED,
            .bclk = EXAMPLE_STD_BCLK_IO1,
            .ws = EXAMPLE_STD_WS_IO1,
            .dout = OUT2, // UNNEEDED!
            // FIX 2: DIN was set to UNUSED. Use the defined DIN pin (33).
            .din = IN2,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    /* Initialize the channels */
    ESP_ERROR_CHECK(i2s_channel_init_std_mode(chan2, &std_cfg1));

    ESP_ERROR_CHECK(i2s_channel_init_std_mode(chan4, &std_cfg2));
}

void app_main(void)
{
    i2s_example_init_std_duplex();

    // --- Variables for I/O (Read) ---
    uint8_t *buf1 = (uint8_t *)calloc(1, EXAMPLE_BUFF_SIZE);
    assert(buf1);
    size_t byte1 = 0;

    uint8_t *buf2 = (uint8_t *)calloc(1, EXAMPLE_BUFF_SIZE);
    assert(buf2);
    size_t byte2 = 0;

    uint8_t *buf3 = (uint8_t *)calloc(1, EXAMPLE_BUFF_SIZE);
    assert(buf3);
    size_t byte3 = 0;

    uint8_t *buf4 = (uint8_t *)calloc(1, EXAMPLE_BUFF_SIZE);
    assert(buf4);
    size_t byte4 = 0;

    // Step 3: Enable TX and RX channels
    ESP_ERROR_CHECK(i2s_channel_enable(chan2));
    ESP_ERROR_CHECK(i2s_channel_enable(chan4));

    printf("I2S Duplex Loop Running without FreeRTOS Tasks...\n");

    /* Step 4: Run the continuous I/O loop in app_main */
    while (1)
    {

        int64_t timestamp_us = esp_timer_get_time();
        double timestamp_s = (double)timestamp_us / 1000000.0;

        if (i2s_channel_read(chan2, buf2, EXAMPLE_BUFF_SIZE, &byte2, 100) == ESP_OK)
        {
            printf("chan2 %d bytes\n-----------------------------------\n", byte2);
            printf("[0] %x [1] %x [2] %x [3] %x\n[4] %x [5] %x [6] %x [7] %x\n\n",
                   buf2[0], buf2[1], buf2[2], buf2[3], buf2[4], buf2[5], buf2[6], buf2[7]);
            save_first_stereo_sample(buf2);
        }
        else
        {
            printf("chan2 down");
        }
        if (i2s_channel_read(chan4, buf4, EXAMPLE_BUFF_SIZE, &byte4, 100) == ESP_OK)
        {
            printf("chan4 %d bytes\n-----------------------------------\n", byte4);
            printf("[0] %x [1] %x [2] %x [3] %x\n[4] %x [5] %x [6] %x [7] %x\n\n",
                   buf4[0], buf4[1], buf4[2], buf4[3], buf4[4], buf4[5], buf4[6], buf4[7]);
            save_first_stereo_sample(buf4);
        }
        else
        {
            printf("chan4 down");
        }

        // Delay to yield and prevent log spamming
        vTaskDelay(pdMS_TO_TICKS(200));
    }
}
