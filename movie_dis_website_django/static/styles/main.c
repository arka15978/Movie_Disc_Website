void init_PWM(){
    PWME_PWME0 = 1;    // Enable channel 0 
    PWMPOL_PPLO0 = 1;  // Polarity for channel 0 set to 1
    PWMCLK_PCLK0 = 1;  //Clock A is the source for channel 0
    PWMPRCLK = 0b00000000;  //Default bus clock frequency of clock A
    PWMPER0 = 255;
    PWMDTY0 = 10;}

void init_PWM_for_motor(){
    PWME_PWME5 = 1;
    PWMPOL_PPLO5 = 1;
    PWMCLK_PCLK5 = 1;
    PWMPRCLK = 0b00000000;
    PWMPER5 = 400;
    PWMDTY5 = 200;

    
}

void init_PIM(){
    DDRA = 0b11111111;
    DDRB = 0;
}

main{
    init_PIM()
    init_PWM()
    init_PWM_for_motor()


}
void interrupt 66 pit(){
    PORTA = 0x00;
    U_DATA = PORTB;
    PORTA = 0x04;
    L_DATA = PORTB;
    en_read = (U_DATA<<8)|L_DATA;
    PORTA = 0x08;


}