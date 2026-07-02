function result = constraint_test_runner()
    % Runs the feasibility study and returns 1 if all PASS
    try
        feasibility_study;
        result = 1;
    catch
        result = 0;
    end
end
