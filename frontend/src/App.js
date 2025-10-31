import React, { useState, useEffect } from 'react';
import { Search, X, Droplet, Sun, Sprout } from 'lucide-react';

const API_URL = 'http://localhost:5000';

export default function PlantasCatalogo() {
  const [plantas, setPlantas] = useState([]);
  const [plantasFiltradas, setPlantasFiltradas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoriasSelecionadas, setCategoriasSelecionadas] = useState([]);
  const [plantaSelecionada, setPlantaSelecionada] = useState(null);
  const [loading, setLoading] = useState(true);

  const categorias = [
    'Arbustos e Árvores',
    'Ervas e Plantas de Vaso',
    'Cactos e Suculentas',
    'Trepadeiras e Outras'
  ];

  useEffect(() => {
    fetchPlantas();
  }, []);

  useEffect(() => {
    filtrarPlantas();
  }, [searchTerm, categoriasSelecionadas, plantas]);

  const fetchPlantas = async () => {
    try {
      const response = await fetch(`${API_URL}/plantas`);
      const data = await response.json();
      console.log(data)
      setPlantas(data.plantas || []);
      setPlantasFiltradas(data.plantas || []);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar plantas:', error);
      setLoading(false);
    }
  };

  const filtrarPlantas = () => {
    let resultado = plantas;

    if (searchTerm) {
      resultado = resultado.filter(planta =>
        planta.nome_popular.toLowerCase().includes(searchTerm.toLowerCase()) ||
        planta.nome_cientifico.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (categoriasSelecionadas.length > 0) {
      resultado = resultado.filter(planta =>
        categoriasSelecionadas.includes(planta.categoria)
      );
    }

    setPlantasFiltradas(resultado);
  };

  const toggleCategoria = (categoria) => {
    setCategoriasSelecionadas(prev =>
      prev.includes(categoria)
        ? prev.filter(c => c !== categoria)
        : [...prev, categoria]
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <header className="bg-green-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Sprout size={36} />
            Catálogo de Plantas Brasileiras
          </h1>
          <p className="text-green-100 mt-2">Explore a diversidade da flora brasileira</p>
        </div>
      </header>
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Buscar por nome popular ou científico..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border-2 border-green-200 rounded-lg focus:outline-none focus:border-green-500 transition"
              />
            </div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Filtrar por Categoria:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
              {categorias.map(categoria => (
                <label
                  key={categoria}
                  className="flex items-center gap-2 cursor-pointer hover:bg-green-50 p-2 rounded transition"
                >
                  <input
                    type="checkbox"
                    checked={categoriasSelecionadas.includes(categoria)}
                    onChange={() => toggleCategoria(categoria)}
                    className="w-4 h-4 text-green-600 rounded focus:ring-2 focus:ring-green-500"
                  />
                  <span className="text-sm text-gray-700">{categoria}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            {plantasFiltradas.length} planta{plantasFiltradas.length !== 1 ? 's' : ''} encontrada{plantasFiltradas.length !== 1 ? 's' : ''}
          </div>
        </div>
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600">Carregando plantas...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {plantasFiltradas.map(planta => (
              <div
                key={planta.id}
                onClick={() => setPlantaSelecionada(planta)}
                className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transform transition hover:scale-105 hover:shadow-xl"
              >
                <div className="h-48 overflow-hidden bg-gray-200">
                  <img
                    src={planta.imagem}
                    alt={planta.nome_popular}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-bold text-green-800 mb-1">{planta.nome_popular}</h3>
                  <p className="text-sm text-gray-600 italic">{planta.nome_cientifico}</p>
                  <span className="inline-block mt-3 px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                    {planta.categoria}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {plantasFiltradas.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Nenhuma planta encontrada com os filtros aplicados.</p>
          </div>
        )}
      </div>
      {plantaSelecionada && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="relative">
              <img
                src={plantaSelecionada.imagem}
                alt={plantaSelecionada.nome_popular}
                className="w-full h-64 object-cover"
              />
              <button
                onClick={() => setPlantaSelecionada(null)}
                className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition"
              >
                <X size={24} />
              </button>
            </div>

            <div className="p-6">
              <h2 className="text-3xl font-bold text-green-800 mb-2">{plantaSelecionada.nome_popular}</h2>
              <p className="text-lg text-gray-600 italic mb-4">{plantaSelecionada.nome_cientifico}</p>
              
              <span className="inline-block mb-6 px-4 py-2 bg-green-100 text-green-700 rounded-full">
                {plantaSelecionada.categoria}
              </span>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Sprout className="text-green-600" size={20} />
                    <h3 className="font-semibold text-gray-800">Altura Média</h3>
                  </div>
                  <p className="text-gray-700">{plantaSelecionada.altura_media_metros} metros</p>
                </div>

                <div className="bg-amber-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Sun className="text-amber-600" size={20} />
                    <h3 className="font-semibold text-gray-800">Época de Floração</h3>
                  </div>
                  <p className="text-gray-700">{plantaSelecionada.epoca_floracao}</p>
                </div>

                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Droplet className="text-blue-600" size={20} />
                    <h3 className="font-semibold text-gray-800">Volume de Água</h3>
                  </div>
                  <p className="text-gray-700">{plantaSelecionada.sugestao_volume_agua_litros} litros</p>
                </div>

                <div className="bg-cyan-50 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Droplet className="text-cyan-600" size={20} />
                    <h3 className="font-semibold text-gray-800">Frequência de Rega</h3>
                  </div>
                  <p className="text-gray-700">{plantaSelecionada.frequencia_rega_geral}</p>
                </div>
              </div>

              <button
                onClick={() => setPlantaSelecionada(null)}
                className="mt-6 w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition font-semibold"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}