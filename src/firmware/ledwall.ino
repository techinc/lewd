#include <SPI.h>

void setup()
{
    Serial.begin(115200);
    SPI.begin();
    SPI.setBitOrder(MSBFIRST);
    SPI.setDataMode(SPI_MODE0);
    SPI.setClockDivider(SPI_CLOCK_DIV16);
}

void loop()
{
    uint8_t c;

	for(;;)
	{
		while (!Serial.available()) {}

		if ( (c = Serial.read()) == 254 )
			break;

        SPI.transfer(c);
	}
    delay(1);
}
