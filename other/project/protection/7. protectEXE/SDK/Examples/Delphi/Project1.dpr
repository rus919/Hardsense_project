program Project1;

uses
  Forms,
  Unit1 in 'Unit1.pas' {Form1},
  SELicenseSDK in 'SELicenseSDK.pas',
  SESDK in 'SESDK.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  Application.Run;
end.
