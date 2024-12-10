
--                          FUNCION Y TRIGGER PARA ACTUALIZAR EL NUMERO DE ENVIOS EN ACTIVITY TABLE EN FUNCION DE USER_ACTIVITY TABLE   
  
  
  
                                    
  
CREATE OR REPLACE FUNCTION update_activity_shipments()
RETURNS TRIGGER AS $$
BEGIN
    -- si se inserta, number_of_shippments ++
    IF TG_OP = 'INSERT' THEN
        UPDATE activity
        SET number_of_shipments = number_of_shipments + 1
        WHERE id = NEW.activity_id;

    -- si se elimina, number_of_shippments --  # TODO, estudiar si esto tiene sentido
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE activity
        SET number_of_shipments = number_of_shipments - 1
        WHERE id = OLD.activity_id;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- creacion de trigger
CREATE TRIGGER user_activity_change
AFTER INSERT OR DELETE ON user_activity
FOR EACH ROW
EXECUTE FUNCTION update_activity_shipments();

-- DROP TRIGGER user_activity_change ON user_activity;





--  FUNCION Y TRIGGER PARA MODIFCAR NUMBER_OF_POSIBLE_ASSISTANCE Y NUMBER_OF_DISCARDS EN LA TABLA ACTIVITY EN FUNCION DE USER_ACTIVITY 'possible_assistance: bool'





CREATE OR REPLACE FUNCTION update_activity_possible_assistance_discards()
RETURNS TRIGGER AS $$
BEGIN
    -- Count the number of TRUE assistance for the activity
    UPDATE activity
    SET number_of_possible_assistances = (
        SELECT COUNT(*) FROM user_activity
        WHERE activity_id = NEW.activity_id AND possible_assistance = TRUE
    ),
    -- Count the number of FALSE assistance for the activity
    number_of_discards = (
        SELECT COUNT(*) FROM user_activity
        WHERE activity_id = NEW.activity_id AND possible_assistance = FALSE
    )
    WHERE id = NEW.activity_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER user_activity_update_change
AFTER UPDATE ON user_activity
FOR EACH ROW
EXECUTE FUNCTION update_activity_possible_assistance_discards();





--  FUNCION Y TRIGGER PARA MODIFCAR NUMBER_OF_ASSISTANCE Y NUMBER_OF_DISCARDS EN LA TABLA ACTIVITY EN FUNCION DE USER_ACTIVITY 'assistance: bool'





CREATE OR REPLACE FUNCTION update_activity_assistance()
RETURNS TRIGGER AS $$
BEGIN
    -- Count the number of TRUE assistance for the activity
    UPDATE activity
    SET number_of_assistances = (
        SELECT COUNT(*) FROM user_activity
        WHERE activity_id = NEW.activity_id AND assistance = TRUE
    )
    WHERE id = NEW.activity_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER user_activity_update_assistance
AFTER UPDATE ON user_activity
FOR EACH ROW
EXECUTE FUNCTION update_activity_assistance();

