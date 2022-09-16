<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\CandidateResource;
use App\Models\Candidate;
use Illuminate\Support\Str;





use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Request as FacadesRequest;

class CandidateResourceController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

   // >>> os.path.dirname(sys.executable)
   // 'C:\\Users\\Wenyx\\AppData\\Local\\Programs\\Python\\Python310'
    public function GeraPython()
    {
        //dd('agora ffssaqsqs');
        $comando = exec("C:\Users\Wenyx\AppData\Local\Programs\Python\Python310\python C:\Users\Wenyx\Csvs\gera.py");

        var_dump($comando);


        //$comando = shell_exec('cd C:\Users\Wenyx\Csvs && C:\Users\Wenyx\Csvs\Gerador.py');//ele cria pasta abre cmd mas n executa

        dd('nao passa');



        $process = new Process(['python','C:\Users\Wenyx\Csvs\Gerador.py'],null,['ENV_VAR_NAME' =>
        'C:\Users\Wenyx\AppData\Local\Programs\Python\Python310']);

        $process->run();

        if (!$process->isSuccessful()){
            throw new ProcessFailedException($process);
        }
        $result = $process->getOutput();

        // $process = Process::fromShellCommandline('inkscape --version');


    }

    public function index(Candidate $candidate)
    {

        $can = Candidate::query()->paginate(10);//->when(request()->get('show') === 'bairro2018',
        //fn($query) => $query->with('bairro2018'))->paginate(3);

        return CandidateResource::collection($can);

    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function show(Candidate $candidate,Request $request)
    {

        if(!request()->get('ANO') or !request()->get('NR_CANDIDATO') ){
            $can = Candidate::query()
            ->where('NM_URNA_CANDIDATO',request()->get('urna'))->paginate(10);
        }

        if(request()->get('ANO')){
            $can = Candidate::query()
            ->when(request()->get('escola') === 'schools2020',fn($query) => $query->with('schools2020'))
            ->when(request()->get('escola') === 'schools2018',fn($query) => $query->with('schools2018'))
            ->when(request()->get('escola') === 'schools2016',fn($query) => $query->with('schools2016'))
            ->when(request()->get('escola') === 'schools2014',fn($query) => $query->with('schools2014'))
            ->when(request()->get('escola') === 'schools2012',fn($query) => $query->with('schools2012'))

            ->when(request()->get('cidade') === 'cities2020',fn($query) => $query->with('cities2020'))
            ->when(request()->get('cidade') === 'cities2018',fn($query) => $query->with('cities2018'))
            ->when(request()->get('cidade') === 'cities2016',fn($query) => $query->with('cities2016'))
            ->when(request()->get('cidade') === 'cities2014',fn($query) => $query->with('cities2014'))
            ->when(request()->get('cidade') === 'cities2012',fn($query) => $query->with('cities2012'))

            ->when(request()->get('bairro') === 'bairro2020',fn($query) => $query->with('bairro2020'))
            ->when(request()->get('bairro') === 'bairro2018',fn($query) => $query->with('bairro2018'))
            ->when(request()->get('bairro') === 'bairro2016',fn($query) => $query->with('bairro2016'))
            ->when(request()->get('bairro') === 'bairro2014',fn($query) => $query->with('bairro2014'))
            ->when(request()->get('bairro') === 'bairro2012',fn($query) => $query->with('bairro2012'))

            ->where([['NM_URNA_CANDIDATO',request()->get('urna')],
            ['ANO_ELEICAO',request()->get('ANO')],
            ['NR_CANDIDATO',request()->get('NR_CANDIDATO')]]
        )->get();
        }

        // $fun = $request->only(['ANO','NR_CANDIDATO']);

        //dd($can);


        if(request()->get('csv')){
            // $ApiPython = $request->fullUrl();
            // //$ApiPython = $request->fullUrlWithoutQuery;

            // $two = '"http://localhost:8000/api/candidatos/candidatos?ANO=2018&NR_CANDIDATO=3133&csv=csv&urna=MARCELO%20ARO"';
            // $twos = "" .$two;

            //$vv = $request->fullUrlWithQuery(['type' => 'phone']);


            //$comando = shell_exec("C:\Users\Wenyx\AppData\Local\Programs\Python\Python310\python C:\Users\Wenyx\Csvs\hello.py {$twos} ");
            $comando = shell_exec("C:\Users\Wenyx\AppData\Local\Programs\Python\Python310\python C:\Users\Wenyx\Csvs\minhaapi.py");


            var_dump($comando);
            //dd($two,$ApiPython,$twos);
        }
        return CandidateResource::collection($can);

    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Candidate $candidate)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function destroy(Candidate $candidate)
    {
        //
    }
}
