package src.main.java.com.estructuradatos.parte1;

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        vecheap<Paciente> vectorHeap = new vecheap<>();
        PriorityQueue<Paciente> pq = new PriorityQueue<>();
        
        // Ruta relativa al archivo
        String filePath = "Parte 1/src/main/resources/pacientes.txt";
        
        try (FileInputStream fis = new FileInputStream(filePath);
             BufferedReader br = new BufferedReader(new InputStreamReader(fis))) {
            
            System.out.println("Leyendo archivo desde: " + new File(filePath).getAbsolutePath());
            
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(", ");
                if (datos.length >= 3) {
                    Paciente paciente = new Paciente(datos[0], datos[1], datos[2].charAt(0));
                    vectorHeap.insert(paciente);
                    pq.offer(paciente);
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Error: Archivo no encontrado en: " + new File(filePath).getAbsolutePath());
            return;
        } catch (IOException e) {
            System.out.println("Error al leer el archivo: " + e.getMessage());
            return;
        }

        System.out.println("Atendiendo con VectorHeap:");
        while (true) {
            Paciente p = vectorHeap.remove();
            if (p == null) break;
            System.out.println(p);
        }

        System.out.println("\nAtendiendo con PriorityQueue de Java:");
        while (!pq.isEmpty()) {
            System.out.println(pq.poll());
        }
    }
}