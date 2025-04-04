package src.test.java;

import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;
import  src.main.java.com.estructuradatos.parte1.Paciente;


public class testComparacionPacientes {
    
    @Test
    void testComparacionPacientes() {
        Paciente p1 = new Paciente("Juan", "Dolor", 'A');
        Paciente p2 = new Paciente("Ana", "Fiebre", 'C');
        assertTrue(p1.compareTo(p2) < 0);
    }
    
    @Test
    void testPrioridadIgual() {
        Paciente p1 = new Paciente("Juan", "Dolor", 'B');
        Paciente p2 = new Paciente("Ana", "Fiebre", 'B');
        assertTrue(p1.compareTo(p2) == 0);
    }
    
    @Test
    void testPrioridadMayor() {
        Paciente p1 = new Paciente("Juan", "Dolor", 'D');
        Paciente p2 = new Paciente("Ana", "Fiebre", 'B');
        assertTrue(p1.compareTo(p2) > 0);
    }
}
